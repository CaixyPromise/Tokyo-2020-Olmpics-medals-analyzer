

# # 连接到SQLite数据库（如果不存在，则会创建一个新的数据库文件）
# conn = sqlite3.connect("medalsDB")
# cursor = conn.cursor()
#
# # 创建用户表单
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT,
#         password_hash TEXT,
#         role INTEGER,
#         group_id TEXT
#     )
# ''')
#
# # 插入示例管理员用户
# password = "admin"  # 实际中应该使用更安全的方式来管理密码
# add_salt_password = register_user(password)
# cursor.execute('''
#     INSERT INTO users (username, password_hash, role, group_id)
#     VALUES (?, ?, ?, ?)
# ''', (
#     "admin",
#     add_salt_password,
#     0,
#     "Admin"
# ))
#
# # 提交更改并关闭连接
# conn.commit()
# # conn.close()
#
#
#
#
# print("用户数据已成功存入SQLite数据库表单。")
#
# # 查询示例管理员用户的哈希密码
# cursor.execute('''
#     SELECT username, password_hash FROM users WHERE username = ?
# ''', ("admin",))
# user_row = cursor.fetchone()
# if user_row:
#     username, hashed_password = user_row
#     login_password = "admin"  # 实际中应该由用户输入
#     print(login_user(login_password, hashed_password))
# else:
#     print("User not found.")
#
# conn.close()


# import ctypes
#
# class LoadDynamicLib:
#     def __init__(self, lib_path = 'utils/DS/DynamicLibaray.dll') -> None:
#         self.lib = ctypes.cdll.LoadLibrary(lib_path)
#         self.lib.init_arr()
#         self.lib.print_arr()
#
# LoadDynamicLib()

# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# def main():
#     root = tk.Tk()
#     root.title("Treeview with Images")
#
#     # Create a Treeview widget
#     tree = ttk.Treeview(root, columns=("Name", "Age"), show='tree headings')
#     tree.heading("#0", text = "Tree Column")
#     tree.heading("#1", text="Name")
#     tree.heading("#2", text="Age")
#
#     # Add data
#     tree.insert("", tk.END, values=("Alice", 30))
#     tree.insert("", tk.END, values=("Bob", 40))
#
#     image = Image.open('static/image/flags/CAN.png')
#
#     image = image.resize((33, 22))
#     photo = ImageTk.PhotoImage(image)
#     # Create a PhotoImage object
#
#     # Insert a row with an image
#     tree.insert("", tk.END, image=photo, values=("Charlie", 50))
#
#     tree.pack()
#
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()

# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
#
#
# def open_image_file(file):
#     image = Image.open(file)
#     image = image.resize((33, 22))
#     photo = ImageTk.PhotoImage(image)
#     return photo
# def main():
#     root = tk.Tk()
#     root.title("Olympics Medal Table")
#     style = ttk.Style()
#     # Set up the Treeview columns
#     tree = ttk.Treeview(root, columns = ("Country", "Gold", "Silver", "Bronze", "Total"), show = 'tree headings')
#     gold_img = open_image_file(file="static/image/gold_medal.png")
#     silver_img = open_image_file(file="static/image/silver_medal.png")
#     bronze_img = open_image_file(file="static/image/bronze_medal.png")
#     # style.layout("Treeview.Heading", [
#     #     ("Treeview.Heading.image", {"side": "left", "sticky": "", }),
#     #     ("Treeview.Heading.cell", {"sticky": "nswe"}),
#     #     ("Treeview.Heading.text", {"side": "left", "sticky": ""})
#     #     ]
#     #              )
#     tree.heading("#0", text = "排名", anchor = tk.CENTER)
#     tree.heading("#1", text = "国家/地区", anchor = tk.CENTER)
#     tree.heading("#2", text = "金牌", anchor = tk.CENTER, image = gold_img, )
#     tree.heading("#3", text = "银牌", anchor = tk.CENTER, image = silver_img)
#     tree.heading("#4", text = "铜牌", anchor = tk.CENTER, image =  bronze_img)
#     tree.heading("#5", text = "总数", anchor = tk.CENTER)
#
#     tree.column("#0", minwidth = 10, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#1", minwidth = 20, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#2", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#3", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#4", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#5", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#
#     # Insert sample data with flag images
#     china_flag = open_image_file(file = "static/image/flags/CHN.png")
#     usa_flag = open_image_file(file = "static/image/flags/USA.png")
#
#     tree.insert("", tk.END, text = "1", image = china_flag, values = ("China", 38, 32, 18, 88))
#     tree.insert("", tk.END, text = "2", image = usa_flag, values = ("USA", 35, 28, 23, 86))
#
#     tree.pack()
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk

# def on_select():
#     selected_date = cal.get_date()
#     selected_time = f"{hour_spin.get()}:{minute_spin.get()}:{second_spin.get()}"
#
#
# root = tk.Tk()
#
# # 创建 Calendar 控件
# cal = DateEntry(root, date_pattern='y-mm-dd', selectmode = 'readonly')
# cal.pack(padx=10, pady=10)
#
# # 创建 Spinbox 控件用于选择时间
# hour_spin = tk.Spinbox(root, from_=0, to=23, width=5, wrap = True, format="%02.0f")
# minute_spin = tk.Spinbox(root, from_=0, to=59, width=5, wrap = True, format="%02.0f")
# second_spin = tk.Spinbox(root, from_=0, to=59, width=5, wrap = True, format="%02.0f")
#
# hour_spin.pack(side=tk.LEFT, padx=(10,0))
# tk.Label(root, text=":").pack(side=tk.LEFT)
# minute_spin.pack(side=tk.LEFT)
# tk.Label(root, text=":").pack(side=tk.LEFT)
# second_spin.pack(side=tk.LEFT, padx=(0,10))
#
# # 创建按钮用于获取选定的日期和时间
# btn = ttk.Button(root, text="Select", command=on_select)
# btn.pack(pady=10)
#
# root.mainloop()

# s = '我是?'
# print(s.upper())
import tkinter
from time import sleep
from itertools import count
from threading import Thread, Event
from tkinter.filedialog import askopenfilename
import pyaudio
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip

root = tkinter.Tk()
root.title("视频播放器-董付国")
root.geometry('860x640+200+100')

isplaying = False
sync_event = Event()  # Added for synchronization

# 用来显示视频画面的Label组件，自带双缓冲，不闪烁
lbVideo = tkinter.Label(root, bg='white')
lbVideo.pack(fill=tkinter.BOTH, expand=tkinter.YES)

def play_video(video):
    global sync_event
    vw = video.w
    vh = video.h
    # 逐帧播放画面
    for frame in video.iter_frames(fps=video.fps/2.5):
        if not isplaying:
            break
        if not sync_event.is_set():
            sync_event.wait()
        w = root.winfo_width()
        h = root.winfo_height()
        # 保持原视频的纵横比
        ratio = min(w/vw, h/vh)
        size = (int(vw*ratio), int(vh*ratio))
        frame = Image.fromarray(frame).resize(size)
        frame = ImageTk.PhotoImage(frame)
        lbVideo['image'] = frame
        lbVideo.image = frame
        lbVideo.update()

def play_audio(audio):
    global sync_event
    p = pyaudio.PyAudio()
    # 创建输出流
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=44100, output=True)
    sync_event.set()
    # 逐帧播放音频
    for chunk in audio.iter_frames():
        if not isplaying:
            break
        stream.write(chunk.astype('float32').tostring())
    p.terminate()

# 创建主菜单
mainMenu = tkinter.Menu(root)

# 创建子菜单
subMenu = tkinter.Menu(mainMenu, tearoff=0)

def open_video():
    global isplaying, sync_event
    isplaying = False
    sync_event.clear()  # Reset the event
    fn = askopenfilename(title='打开视频文件', filetypes=[("视频", "*.mp4 *.avi")])
    if fn:
        root.title(f'视频播放器-董付国-正在播放 "{fn}"')
        video = VideoFileClip(fn)
        audio = video.audio
        isplaying = True
        # 播放视频的线程
        t1 = Thread(target=play_video, args=(video,))
        t1.daemon = True
        t1.start()
        # 播放音频的线程
        t2 = Thread(target=play_audio, args=(audio,))
        t2.daemon = True
        t2.start()

# 添加菜单项，设置命令
subMenu.add_command(label='打开视频文件', command=open_video)

# 把子菜单挂到主菜单上
mainMenu.add_cascade(label='文件', menu=subMenu)

# 把主菜单放置到窗口上
root['menu'] = mainMenu

# 确保子线程关闭
def exiting():
    global isplaying
    isplaying = False
    sleep(0.95)
    root.destroy()

root.protocol('WM_DELETE_WINDOW', exiting)
root.mainloop()
