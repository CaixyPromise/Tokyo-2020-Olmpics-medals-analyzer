import tkinter.ttk as ttk
import tkinter as tk
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from ui.common.RankTreeview import RankTreeview
from ui.common.RaceTreeview import RaceTreeview
from ui.common.TeamTreeview import TeamTreeview
from ui.common.UserTreeview import UserTreeview

class AdminDialogWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.setup_banner()
        self.init_frame()
        self.setup_command()
        self.setup_display()

    def setup_banner(self):
        top_frame = ttk.Frame(self)
        top_frame.grid(row = 0, column = 0, columnspan = 2, sticky = "WE")
        top_frame.columnconfigure(0, weight = 1)
        top_frame.rowconfigure(0, weight = 1)

        # top_frame.pack(side = "top", fill = "x")
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

    def init_frame(self):
        self.command_frame = ttk.LabelFrame(self, text = '控制台')
        self.command_frame.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 10, pady = 10)
        # self.command_frame.pack(side = 'left', fill = 'both', padx = 10, pady = 10,anchor = tk.NW)
        self.display_frame = ttk.Frame(self,  width = 200)
        self.display_frame.grid(row = 1, column = 1, sticky = "NSEW", padx = 10, pady = 10)
        self.display_frame.update_idletasks()

        self.style = ttk.Style(self)

        # 设置Treeview的字体和大小
        self.tree_font = font.Font(family = "Helvetica", size = 16, )
        self.style.configure("Treeview.Heading", font = self.tree_font )

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
        self.race_mannageBtn = ttk.Button(self.command_frame, text = "比赛项目管理")
        self.race_mannageBtn.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.team_mannageBtn = ttk.Button(self.command_frame, text = "国家队管理")
        self.team_mannageBtn.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.medal_mannageBtn = ttk.Button(self.command_frame, text = "奖牌项目管理")
        self.medal_mannageBtn.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.admin_mannageBtn = ttk.Button(self.command_frame, text = "管理员管理")
        self.admin_mannageBtn.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)

        logo_frame = tk.Frame(self.command_frame)
        logo_frame.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = 10, sticky = tk.NSEW, rowspan = 2)
        logo_label = tk.Label(logo_frame, anchor = "center")
        logo_label.pack(side = "left", fill = "y", expand = True)
        MediaViewer(logo_label).show_image('static/image/Tokyo_2020both_Logo.png', (204, 156))

    def setup_display(self):
        # 设置一个Notebook结构
        self.notebook = ttk.Notebook(self.display_frame)
        self.notebook.pack(fill = 'both', expand = True)

        # 设置一个TreeViewUtils布局，用于显示金牌榜信息：列名：排名、国家/地区、金牌、银牌、铜牌、总数
        self.Goldmedal_infoFrame = ttk.Frame(self.notebook)
        self.Goldmedal_infoFrame.pack(expand = True, fill = "both")
        self.goldRank_scrollbar = ttk.Scrollbar(self.Goldmedal_infoFrame, orient = "vertical", )
        self.goldRank_scrollbar.pack(side = 'right', fill = 'y')
        self.goldRank_tree = RankTreeview(self.Goldmedal_infoFrame)
        self.goldRank_scrollbar.config(command = self.goldRank_tree.yview)
        self.goldRank_tree.configure(yscrollcommand = self.goldRank_scrollbar.set)
        self.goldRank_scrollbar.config(command = self.goldRank_tree.yview)
        self.goldRank_tree.update_idletasks()
        self.notebook.add(self.Goldmedal_infoFrame, text = "金牌榜")

        # 设置一个TreeViewUtils布局，用于显示奖牌榜信息：列名：排名、国家/地区、金牌、银牌、铜牌、总数
        self.medal_infoFrame = ttk.Frame(self.notebook)
        self.medal_infoFrame.pack(expand = True, fill = "both")
        self.MedalRank_scrollbar = ttk.Scrollbar(self.medal_infoFrame, orient = "vertical", )
        self.MedalRank_scrollbar.pack(side = 'right', fill = 'y')
        self.medalRank_tree = RankTreeview(self.medal_infoFrame)
        self.medalRank_tree.configure(yscrollcommand = self.MedalRank_scrollbar.set)
        self.MedalRank_scrollbar.config(command = self.medalRank_tree.yview)
        self.notebook.add(self.medal_infoFrame, text = "奖牌榜")

        self.race_info_frame = ttk.Frame(self.notebook)
        self.race_info_frame.pack(expand = True, fill = "both")
        self.scrollbar = ttk.Scrollbar(self.race_info_frame, )
        self.scrollbar.pack(side = 'right', fill = 'y')
        # 设置一个TreeViewUtils布局，用于显示比赛项目信息，列名：比赛ID、时间、地点、比赛名称、比赛类型，并插入到notebook中
        self.race_tree = RaceTreeview(self.race_info_frame)
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.scrollbar.config(command = self.race_tree.yview)
        self.race_tree.configure(yscrollcommand = self.scrollbar.set)
        self.notebook.add(self.race_info_frame, text = "比赛项目信息")
        self.scrollbar.config(command = self.race_tree.yview)


        # 国家队信息
        self.team_info_frame = ttk.Frame(self.notebook)
        self.team_info_frame.pack(expand = True, fill = "both")
        self.team_scrollbar = ttk.Scrollbar(self.team_info_frame, )
        self.team_scrollbar.pack(side = 'right', fill = 'y')
        self.team_tree = TeamTreeview(self.team_info_frame,
                                      )
        self.team_scrollbar.config(command = self.team_tree.yview)
        self.team_tree.configure(yscrollcommand = self.team_scrollbar.set)
        self.notebook.add(self.team_info_frame, text = "国家队信息")
        self.team_scrollbar.config(command = self.team_tree.yview)

        # 管理员信息
        self.admin_info_frame = ttk.Frame(self.notebook)
        self.admin_info_frame.pack(expand = True, fill = "both")
        self.admin_scrollbar = ttk.Scrollbar(self.admin_info_frame, )
        self.admin_scrollbar.pack(side = 'right', fill = 'y')
        self.admin_tree = UserTreeview(self.admin_info_frame)
        self.admin_scrollbar.config(command = self.admin_tree.yview)
        self.admin_tree.configure(yscrollcommand = self.admin_scrollbar.set)
        self.notebook.add(self.admin_info_frame, text = "管理员信息")
        self.admin_scrollbar.config(command = self.admin_tree.yview)

