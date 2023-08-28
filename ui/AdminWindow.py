import tkinter.ttk as ttk
import tkinter as tk
from ui.utils.TreeviewUtils import TreeViewUtils
from utils.MediaViewer.MediaViewer import  MediaViewer
from  PIL import Image, ImageTk
from tkinter import font
def make_image(file, size = (33, 22)):
    image = Image.open(file)
    image = image.resize(size)
    photo = ImageTk.PhotoImage(image)
    return photo


class AdminWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        top_frame = tk.Frame(self)
        top_frame.pack(side = "top", fill = "x")
        banner_frame = tk.Frame(top_frame)
        banner_frame.pack(side = "left", fill = "x", expand = True)
        banner_label = tk.Label(banner_frame,
                                text = "2020东京奥运会奖牌管理系统 管理员",
                                font = ("Arial", 14), anchor = "center"
                                )
        logo_label = tk.Label(banner_frame, anchor = "center")
        logo_label.pack(side = "left",  fill = "y", expand = True)
        MediaViewer(logo_label).show_image('static/image/Tokyo_2020both_Logo.png', (128, 70))
        # 居中
        banner_label.pack(side = 'left', fill = 'x',  expand = True)

        self.command_frame = ttk.LabelFrame(self, text = '控制台')
        self.command_frame.pack(side = 'left', fill = 'both', padx = 10, pady = 10,anchor = tk.NW)
        self.display_frame = tk.Frame(self,  width = 200)
        self.display_frame.pack_propagate(False)
        self.display_frame.pack(side = 'left', expand = True, fill = 'y',
                                padx = 10, pady = 10,anchor = tk.NW, after = self.command_frame,)
        self.display_frame.configure(width = 900, height =  900)
        self.display_frame.update_idletasks()

        self.style = ttk.Style(self)

        # 设置Treeview的字体和大小
        self.tree_font = font.Font(family = "Helvetica", size = 16, )
        self.style.configure("Treeview.Heading", font = self.tree_font )

        self.setup_command()
        self.setup_display()



    def setup_command(self):
        """
        增加比赛项目信息：管理员可以添加新的比赛项目。
        删除比赛项目信息：管理员可以删除现有的比赛项目。
        修改比赛项目信息：管理员可以修改现有的比赛项目。
        查询比赛项目信息：管理员可以查看所有比赛项目的信息。
        增加/删除/修改/查询 比赛项目获奖信息：与比赛项目信息操作类似。
        增加/删除/修改/查询国家队信息：与比赛项目信息操作类似。
        """
        # 增加比赛信息按钮, grid布局，self实例化，不绑定command参数
        self.add_button = ttk.Button(self.command_frame, text = "增加比赛项目")
        self.add_button.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.delete_button = ttk.Button(self.command_frame, text = "删除比赛项目")
        self.delete_button.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.modify_button = ttk.Button(self.command_frame, text = "修改比赛项目")
        self.modify_button.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.query_button = ttk.Button(self.command_frame, text = "查询比赛项目")
        self.query_button.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.add_team_button = ttk.Button(self.command_frame, text = "增加国家队")
        self.add_team_button.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.delete_team_button = ttk.Button(self.command_frame, text = "删除国家队")
        self.delete_team_button.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.modify_team_button = ttk.Button(self.command_frame, text = "修改国家队")
        self.modify_team_button.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.query_team_button = ttk.Button(self.command_frame, text = "查询国家队")
        self.query_team_button.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        # 增加/删除/修改/查询 比赛项目获奖信息：与比赛项目信息操作类似。
        self.add_award_button = ttk.Button(self.command_frame, text = "增加获奖信息")
        self.add_award_button.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.delete_award_button = ttk.Button(self.command_frame, text = "删除获奖信息")
        self.delete_award_button.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.modify_award_button = ttk.Button(self.command_frame, text = "修改获奖信息")
        self.modify_award_button.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.query_award_button = ttk.Button(self.command_frame, text = "查询获奖信息")
        self.query_award_button.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        # 增加/删除/修改/查询 账号：
        self.mannager_button = ttk.Button(self.command_frame, text = "管理账号")
        self.mannager_button.grid(row = 6, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        # 退出系统
        self.exit_button = ttk.Button(self.command_frame, text = "退出系统")
        self.exit_button.grid(row = 6, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
    def setup_display(self):
        # 设置一个Notebook结构
        self.notebook = ttk.Notebook(self.display_frame)
        self.notebook.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.team_info_frame = ttk.Frame(self.notebook)
        self.team_info_frame.pack(expand = True, fill = "both")
        # 设置一个TreeViewUtils布局，用于显示比赛项目信息，列名：比赛ID、时间、地点、比赛名称、比赛类型，并插入到notebook中
        self.race_infoFrame = TreeViewUtils(self.team_info_frame,
                                            columns = ["比赛ID", "时间", "地点", "比赛名称", "比赛类型"],
                                            show = 'headings',
                                            )
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.scrollbar = ttk.Scrollbar(self.team_info_frame, command = self.race_infoFrame.yview)
        self.scrollbar.pack(side = 'right', fill = 'y')
        self.race_infoFrame.configure(yscrollcommand = self.scrollbar.set)
        self.notebook.add(self.team_info_frame, text = "比赛项目信息")
        self.scrollbar.config(command = self.race_infoFrame.yview)

        # 设置一个TreeViewUtils布局，用于显示奖牌榜信息：列名：排名、国家/地区、金牌、银牌、铜牌、总数
        self.medal_infoFrame = ttk.Frame(self.notebook)
        self.medal_infoFrame.pack(expand = True, fill = "both")
        self.gold_img = make_image(file = "static/image/gold_medal.png")
        self.silver_img = make_image(file = "static/image/silver_medal.png")
        self.bronze_img = make_image(file = "static/image/bronze_medal.png")
        custom_headings = {
            "#0": {"text": "排名", "anchor": tk.CENTER},
            "#1": {"text": "国家/地区", "anchor": tk.CENTER},
            "#2": {"text": "金牌", "anchor": tk.CENTER, "image": self.gold_img},
            "#3": {"text": "银牌", "anchor": tk.CENTER, "image": self.silver_img},
            "#4": {"text": "铜牌", "anchor": tk.CENTER, "image": self.bronze_img},
            "#5": {"text": "总数", "anchor": tk.CENTER}
            }

        custom_columns = {
            "#0": {"minwidth": 10, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#1": {"minwidth": 20, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#2": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#3": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#4": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#5": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'}
            }

        self.medal_tree = TreeViewUtils(self.medal_infoFrame,
                                        columns =  ["排名", "国家/地区", "金牌", "银牌", "铜牌", "总数"],
                                        custom_headings = custom_headings,
                                        custom_columns = custom_columns,
                                        show = 'tree headings',
                                        )
        self.medal_scrollbar = ttk.Scrollbar(self.medal_infoFrame, orient = "vertical", command = self.medal_tree.yview)
        self.medal_scrollbar.pack(side = 'right', fill = 'y')
        self.medal_tree.configure(yscrollcommand = self.medal_scrollbar.set)
        self.medal_scrollbar.config(command = self.medal_tree.yview)
        self.notebook.add(self.medal_infoFrame, text = "奖牌榜")
