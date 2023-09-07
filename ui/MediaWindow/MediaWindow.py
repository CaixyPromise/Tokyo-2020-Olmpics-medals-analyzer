import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
import tkinter.ttk as ttk

import cv2
import random
import time
from tkinter.filedialog import askopenfilename
from decimal import Decimal
from tkinter import *
from ffpyplayer.player import MediaPlayer
from PIL import Image, ImageTk
import tempfile
import threading
import queue
import os
import sys
import contextlib


class VideoPlayer:
    def __init__(self, root, file, **kwargs):

        self.dest = file
        self.cap = cv2.VideoCapture(self.dest)

        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.newfps = self.fps
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.root = root
        # self.root.overrideredirect(1)
        self.root.geometry('+0+0')
        self.resize = False
        self.is_destroyed = False  # Add this line to track if the application is destroyed
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.kill())  # Add this line to handle window close event

        for k, val in kwargs.items():
            if k == "fps":
                if val > self.fps:
                    print("Error: requested FPS is higher than file FPS")
                    self.root.destroy()
                    return
                self.newfps = val
            elif k == "pos":
                self.root.geometry("+%d+%d" % val)
            elif k == "draggable" and val == True:
                self.root.bind('<Button-1>', self.clickPos)
                self.root.bind('<B1-Motion>', self.dragWin)
                self.clickx = None
                self.clicky = None
            elif k == "dim":
                if (val[0] == self.width and val[1] == self.height):
                    continue
                self.width = val[0]
                self.height = val[1]
                self.resize = True
            elif k == "videoOptions" and val == True:
                self.root.bind('<Button-3>', self.options)

    def play(self):
        self.root.deiconify()

        self.canvas = Canvas(self.root, width = self.width, height = self.height)
        self.canvas.pack()

        self.fr_lock = threading.Lock()
        self.frames_read = queue.Queue()
        self.frame_files = queue.Queue()  # list of temp files
        self.frame_times = []
        self.kill_threads = False

        self.player = MediaPlayer(self.dest)
        self.player.set_pause(True)

        time.sleep(1)

        self.t1 = threading.Thread(target = self.readFrames)
        self.t2 = threading.Thread(target = self.writeFrames)
        self.t3 = threading.Thread(target = self.writeFrames)

        self.t1.start()
        time.sleep(2)
        self.t2.start()
        self.t3.start()
        time.sleep(1)

        self.playVideo()

        self.t1.join()
        self.t2.join()
        self.t3.join()

    def clickPos(self, event):
        time.sleep(.2)
        self.clickx = event.x
        self.clicky = event.y

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.player.set_pause(False)  # 恢复音频播放
            self.pause_event.set()  # 恢复视频播放
        else:
            self.is_paused = True
            self.player.set_pause(True)  # 暂停音频播放
            self.pause_event.clear()  # 暂停视频播放

    def dragWin(self, event):
        winx = self.root.winfo_x()
        winy = self.root.winfo_y()

        x = event.x - self.clickx + winx
        y = event.y - self.clicky + winy
        self.root.geometry("+%d+%d" % (x, y))

    def kill(self):
        if (not self.kill_threads):
            self.kill_threads = True
            self.is_destroyed = True
            self.player.set_pause(True)
            self.root.destroy()
            exit(1)

    def options(self, event):

        def restart():
            os.execl(sys.executable, sys.executable, *sys.argv)

        m = Menu(self.root, tearoff = 0)
        m.add_command(label = "restart", command = restart)
        m.add_command(label = "quit", command = self.kill)
        m.tk_popup(event.x_root, event.y_root)

    def randSelect(self):
        frameList = []
        accuracy = 2

        ratio = round(self.newfps / self.fps, accuracy)
        dec_ratio = Decimal(str(ratio))
        self.newfps = ratio * self.fps
        b = (dec_ratio).as_integer_ratio()

        frame_guarantee = b[0]
        frame_chunk = b[1]

        for i in range(1, self.frames, frame_chunk):
            select = range(i, i + frame_chunk - 1)
            samp = random.sample(select, frame_guarantee)
            samp.sort()
            frameList.extend(samp)

        return frameList

    def generateFrameTimes(self):
        newFrames = int(self.frames * self.newfps / self.fps)

        targetTime = 1 / self.newfps
        times = 0

        for i in range(newFrames):
            self.frame_times.append(times)
            times += targetTime

    def readFrames(self):
        if (self.fps == self.newfps):
            self.generateFrameTimes()
            while (self.cap.isOpened()):
                if (self.kill_threads == True):
                    return

                if (self.frames_read.qsize() > 10):
                    time.sleep(.01)
                    continue

                ret, frame = self.cap.read()
                if ret == True:
                    self.frames_read.put(frame)
                else:
                    break
        else:

            select_list = self.randSelect()
            self.generateFrameTimes()

            counter = 0
            walker = 0

            while (self.cap.isOpened()):
                if (self.kill_threads == True):
                    return

                if (self.frames_read.qsize() > 10):
                    time.sleep(.01)
                    continue

                counter += 1
                ret, frame = self.cap.read()
                if ret == False:
                    break

                if (select_list[walker] == counter):
                    self.frames_read.put(frame)

                    walker += 1

    @contextlib.contextmanager
    def make_temp_directory(self):
        temp_dir = tempfile.TemporaryDirectory()
        try:
            yield temp_dir
        finally:
            temp_dir.cleanup()

    def writeFrames(self):

        with self.make_temp_directory() as temp_dir:
            while True:

                if (self.kill_threads == True):
                    temp_dir.cleanup()
                    return

                if self.frame_files.qsize() > 20:
                    time.sleep(.1)
                    continue

                p = tempfile.NamedTemporaryFile('wb', suffix = '.jpg',
                                                dir = temp_dir.name,
                                                delete = False
                                                )

                with self.fr_lock:
                    if self.frames_read.empty():
                        break

                    frame = self.frames_read.get()
                    self.frame_files.put(p)

                if self.resize == True:
                    frame = cv2.resize(frame, (self.width, self.height),
                                       interpolation = cv2.INTER_AREA
                                       )

                cv2.imwrite(p.name, frame)
                p.close()

    def playVideo(self):
        counter = 0

        fps = self.newfps  # for testing max frame rate
        targetTime = 1 / fps
        self.is_paused = False  # 控制暂停的状态变量
        self.pause_event = threading.Event()
        self.pause_event.set()  # 初始设置为非暂停状态

        img = None
        pop = None
        self.player.set_pause(False)

        # load up the audio
        audio_frame, val = self.player.get_frame()
        while audio_frame is None:
            audio_frame, val = self.player.get_frame()

        running_time = time.time()
        while (not self.frame_files.empty() and not self.is_destroyed):
            self.pause_event.wait()
            if (self.kill_threads == True):
                return

            audio_frame, val = self.player.get_frame()

            if (val == 'eof' or len(self.frame_times) == 0):
                break

            if (audio_frame == None):
                continue

            # for any lag due to cpu, especially for dragging
            if (self.frame_files.qsize() < 5):
                time.sleep(.08)

            t = self.frame_times.pop(0)
            pop = self.frame_files.get()

            cur_time = time.time() - running_time
            delay = t - cur_time

            # frame skipping
            if (delay < -targetTime):
                os.remove(pop.name)
                continue

            prevIm = img

            # diplay image
            self.canvas.delete("all")

            try:
                load = Image.open(pop.name)
            except:
                os.remove(pop.name)
                continue

            # load.draft("RGB",(2560,1080)) # doesn't do anything?
            render = ImageTk.PhotoImage(load)
            img = Label(image = render)
            img.image = render
            img.place(x = 0, y = 0)
            load.close()
            pop.close()

            os.remove(pop.name)

            self.root.update()

            if prevIm is not None and not self.is_destroyed:
                prevIm.destroy()

            cur_time = time.time() - running_time
            delay = t - cur_time

            if (delay > targetTime):
                time.sleep(targetTime)

        self.kill()

class MediaDialogWindow(ttk.Frame):
    '''继承自Frame类，master为Tk类顶级窗体（带标题栏、最大、最小、关闭按钮）'''

    def __init__(self, master = None):
        super().__init__(master)
        self.initComponent(master)

    def play(self):
        '''播放'''
        self.play_button.config(text = '暂停')
        self.play_button.config(command = self.pause)
        self.master.after(1000, self.play_loop)
    def pause(self):
        '''暂停'''
        self.play_button.config(text = '播放')
        self.play_button.config(command = self.play)
    def play_loop(self):
        '''播放循环'''
        self.play()
    def kill(self):

    def initComponent(self, master):
        '''初始化GUI组件'''
        master.rowconfigure(0, weight = 1);
        master.columnconfigure(0, weight = 1)
        self.ft = tkFont.Font(family = '微软雅黑', size = 12, weight = 'bold')  # 创建字体
        self.initMenu(master)  # 为顶级窗体添加菜单项
        # 设置继承类MWindow的grid布局位置，并向四个方向拉伸以填充顶级窗体
        self.grid(row = 0, column = 0, sticky = tk.NSEW)
        # 设置继承类MWindow的行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0, weight = 1);
        self.columnconfigure(0, weight = 1)

        self.panewin = ttk.Panedwindow(self, orient = tk.HORIZONTAL)  # 添加水平方向的推拉窗组件
        self.panewin.grid(row = 0, column = 0, sticky = tk.NSEW)  # 向四个方向拉伸填满MWindow帧

        self.frm_left = ttk.Frame(self.panewin, relief = tk.SUNKEN, padding = 0)  # 左侧Frame帧用于放置播放列表
        self.frm_left.grid(row = 0, column = 0, sticky = tk.NS);  # 左侧Frame帧拉伸填充
        self.panewin.add(self.frm_left, weight = 1)  # 将左侧Frame帧添加到推拉窗控件，左侧权重1
        self.initPlayList()  # 添加树状视图

        self.frm_right = ttk.Frame(self.panewin, relief = tk.SUNKEN)  # 右侧Frame帧用于放置视频区域和控制按钮
        self.frm_right.grid(row = 0, column = 0, sticky = tk.NSEW)  # 右侧Frame帧四个方向拉伸
        self.frm_right.columnconfigure(0, weight = 1);  # 右侧Frame帧两行一列，配置列的权重
        self.frm_right.rowconfigure(0, weight = 8);  # 右侧Frame帧两行的权重8:1
        self.frm_right.rowconfigure(1, weight = 1)
        self.panewin.add(self.frm_right, weight = 50)  # 将右侧Frame帧添加到推拉窗控件,右侧权重10

        s = ttk.Style();
        s.configure('www.TFrame', background = 'black')  # 视频区Frame帧添加样式
        # 右侧Frame帧第一行添加视频区Frame
        self.frm_vedio = ttk.Frame(self.frm_right, relief = tk.RIDGE, style = 'www.TFrame')
        self.frm_vedio.grid(row = 0, column = 0, sticky = tk.NSEW)
        # 右侧Frame帧第二行添加控制按钮
        self.frm_control = ttk.Frame(self.frm_right, relief = tk.RAISED)  # 四个方向拉伸
        self.frm_control.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.initCtrl()  # 添加滑块及按钮

    def initMenu(self, master):
        '''初始化菜单'''
        mbar = tk.Menu(master)  # 定义顶级菜单实例
        fmenu = tk.Menu(mbar, tearoff = False)  # 在顶级菜单下创建菜单项
        mbar.add_cascade(label = ' 文件 ', menu = fmenu, font = ('Times', 20, 'bold'))  # 添加子菜单
        fmenu.add_command(label = "打开", command = self.menu_click_event)
        fmenu.add_command(label = "保存", command = self.menu_click_event)
        fmenu.add_separator()  # 添加分割线
        fmenu.add_command(label = "退出", command = master.quit())

        etmenu = tk.Menu(mbar, tearoff = False)
        mbar.add_cascade(label = ' 编辑 ', menu = etmenu)
        for each in ['复制', '剪切', '合并']:
            etmenu.add_command(label = each, command = self.menu_click_event)
        master.config(menu = mbar)  # 将顶级菜单注册到窗体

    def menu_click_event(self):
        '''菜单事件'''
        pass

    def initPlayList(self):
        '''初始化树状视图'''
        self.frm_left.rowconfigure(0, weight = 1)  # 左侧Frame帧行列权重配置以便子元素填充布局
        self.frm_left.columnconfigure(0, weight = 1)  # 左侧Frame帧中添加树状视图
        tree = ttk.Treeview(self.frm_left, selectmode = 'browse', show = 'tree', padding = [0, 0, 0, 0])
        tree.grid(row = 0, column = 0, sticky = tk.NSEW)  # 树状视图填充左侧Frame帧
        tree.column('#0', width = 150)  # 设置图标列的宽度，视图的宽度由所有列的宽决定
        # 一级节点parent='',index=第几个节点,iid=None则自动生成并返回，text为图标右侧显示文字
        # values值与columns给定的值对应
        tr_root = tree.insert("", 0, None, open = True, text = '播放列表')  # 树视图添加根节点
        node1 = tree.insert(tr_root, 0, None, open = True, text = '本地文件')  # 根节点下添加一级节点
        node11 = tree.insert(node1, 0, None, text = '文件1')  # 添加二级节点
        node12 = tree.insert(node1, 1, None, text = '文件2')  # 添加二级节点
        node2 = tree.insert(tr_root, 1, None, open = True, text = '网络文件')  # 根节点下添加一级节点
        node21 = tree.insert(node2, 0, None, text = '文件1')  # 添加二级节点
        node22 = tree.insert(node2, 1, None, text = '文件2')  # 添加二级节点

    def initCtrl(self):
        '''初始化控制滑块及按钮'''
        self.frm_control.columnconfigure(0, weight = 1);  # 配置控制区Frame各行列的权重
        self.frm_control.rowconfigure(0, weight = 1);  # 第一行添加滑动块
        self.frm_control.rowconfigure(1, weight = 1);  # 第二行添加按钮
        slid = ttk.Scale(self.frm_control, from_ = 0, to = 900, command = self.sliderValueChanged)
        slid.grid(row = 0, column = 0, sticky = tk.EW, padx = 2)  # 滑动块水平方向拉伸

        frm_but = ttk.Frame(self.frm_control, padding = 2)  # 控制区第二行放置按钮及标签
        frm_but.grid(row = 1, column = 0, sticky = tk.EW)
        self.lab_curr = ttk.Label(frm_but, text = "00:00:00", font = self.ft)  # 标签显示当前时间
        lab_max = ttk.Label(frm_but, text = "00:00:00", font = self.ft)  # 标签显示视频长度
        self.lab_curr.grid(row = 0, column = 0, sticky = tk.W, padx = 3)
        lab_max.grid(row = 0, column = 13, sticky = tk.E, padx = 3)
        i = 4
        for but in ['播放', '暂停', '快进', '快退', '静音']:
            ttk.Button(frm_but, text = but).grid(row = 0, column = i)
            i += 1
        for i in range(14):  # 为每列添加权重值以便水平拉伸
            frm_but.columnconfigure(i, weight = 1)

    def sliderValueChanged(self, val):
        '''slider改变滑块值的事件'''
        # tkinter.messagebox.showinfo("Message", "message")
        flt = float(val);
        strs = str('%.1f' % flt)
        self.lab_curr.config(text = strs)

if(__name__=='__main__'):
    root = tk.Tk()
    root.geometry('800x480+200+100')
    root.title('Media Player')
    #root.option_add("*Font", "宋体")
    root.minsize(800, 480)
    app = MediaDialogWindow(root)
    root.mainloop()
