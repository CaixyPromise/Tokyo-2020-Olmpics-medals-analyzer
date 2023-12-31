import tkinter.ttk as ttk
import tkinter as tk

from ui.common.MedalInfoTreeview import MedalRaceInfoTreeview
from ui.common.RaceTeamTreeview import RaceTeamTreeview
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from ui.common.RankTreeview import RankTreeview
from ui.common.RaceTreeview import RaceTreeview


class PlayerDialogWindow(ttk.Frame):
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
                                text = "2020东京奥运会奖牌管理系统 运动员中心",
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
        self.race_mannageBtn = ttk.Button(self.command_frame, text = "我的比赛管理")
        self.race_mannageBtn.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.NSEW)
        self.reward_mannageBtn = ttk.Button(self.command_frame, text = "我的夺冠时刻")
        self.reward_mannageBtn.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = tk.NSEW)
        self.exit_systemBTN = ttk.Button(self.command_frame, text = "退出系统")
        self.exit_systemBTN.grid(row = 1, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = tk.NSEW)

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

        # 金牌榜顶部搜索框
        gold_search_frame = ttk.Frame(self.Goldmedal_infoFrame)
        gold_search_frame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(gold_search_frame, text = "金牌榜搜索", font = ( 'Helvetica', 16,)).pack(side = "left")
        self.goldRankSearch_entry = ttk.Entry(gold_search_frame, width = 80)
        self.goldRankSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.goldRankSearch_button = ttk.Button(gold_search_frame, text = "搜索", width = 10)
        self.goldRankSearch_button.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)

        self.goldRank_scrollbar = ttk.Scrollbar(self.Goldmedal_infoFrame, orient = "vertical")
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
        # 金牌榜顶部搜索框
        medal_searchFrame = ttk.Frame(self.medal_infoFrame)
        medal_searchFrame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(medal_searchFrame, text = "奖牌榜搜索", font = ('Helvetica', 16)).pack(side = "left")
        self.medalRankSearch_entry = ttk.Entry(medal_searchFrame, width = 80)
        self.medalRankSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.medalRankSearch_btn = ttk.Button(medal_searchFrame, text = "搜索")
        self.medalRankSearch_btn.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)

        self.MedalRank_scrollbar = ttk.Scrollbar(self.medal_infoFrame, orient = "vertical", )
        self.MedalRank_scrollbar.pack(side = 'right', fill = 'y')
        self.medalRank_tree = RankTreeview(self.medal_infoFrame)
        self.medalRank_tree.configure(yscrollcommand = self.MedalRank_scrollbar.set)
        self.MedalRank_scrollbar.config(command = self.medalRank_tree.yview)
        self.notebook.add(self.medal_infoFrame, text = "奖牌榜")

        self.race_info_frame = ttk.Frame(self.notebook)
        self.race_info_frame.pack(expand = True, fill = "both")
        race_searchFrame = ttk.Frame(self.race_info_frame)
        race_searchFrame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(race_searchFrame, text = "比赛项目搜索", font = ('Helvetica', 16)).pack(side = "left")
        self.raceRankSearch_entry = ttk.Entry(race_searchFrame, width = 80)
        self.raceRankSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.raceRankSearch_btn = ttk.Button(race_searchFrame, text = "搜索")
        self.raceRankSearch_btn.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)

        self.scrollbar = ttk.Scrollbar(self.race_info_frame, )
        self.scrollbar.pack(side = 'right', fill = 'y')
        # 设置一个TreeViewUtils布局，用于显示比赛项目信息，列名：比赛ID、时间、地点、比赛名称、比赛类型，并插入到notebook中
        self.race_tree = RaceTreeview(self.race_info_frame)
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.scrollbar.config(command = self.race_tree.yview)
        self.race_tree.configure(yscrollcommand = self.scrollbar.set)
        self.notebook.add(self.race_info_frame, text = "比赛项目信息")
        self.scrollbar.config(command = self.race_tree.yview)


        self.play_race_info_frame = ttk.Frame(self.notebook)
        self.play_race_info_frame.pack(expand = True, fill = "both")
        play_race_searchFrame = ttk.Frame(self.play_race_info_frame)
        play_race_searchFrame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(play_race_searchFrame, text = "比赛项目搜索", font = ('Helvetica', 16)).pack(side = "left")
        self.play_raceRankSearch_entry = ttk.Entry(play_race_searchFrame, width = 80)
        self.play_raceRankSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.play_raceRankSearch_btn = ttk.Button(play_race_searchFrame, text = "搜索")
        self.play_raceRankSearch_btn.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)


        self.play_scrollbar = ttk.Scrollbar(self.play_race_info_frame, )
        self.play_scrollbar.pack(side = 'right', fill = 'y')
        self.play_race_tree = RaceTreeview(self.play_race_info_frame)
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.play_scrollbar.config(command = self.play_race_tree.yview)
        self.play_race_tree.configure(yscrollcommand = self.play_scrollbar.set)
        self.notebook.add(self.play_race_info_frame, text = "我的比赛信息")
        self.play_scrollbar.config(command = self.play_race_tree.yview)


        # 各个国家参赛报名比赛信息
        self.race_team_info_frame = ttk.Frame(self.notebook)
        self.race_team_info_frame.pack(expand = True, fill = "both")
        race_team_searchFrame = ttk.Frame(self.race_team_info_frame)
        race_team_searchFrame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(race_team_searchFrame, text = "队员搜索", font = ('Helvetica', 16)).pack(side = "left")
        self.race_teamSearch_entry = ttk.Entry(race_team_searchFrame, width = 80)
        self.race_teamSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.race_teamSearch_btn = ttk.Button(race_team_searchFrame, text = "搜索")
        self.race_teamSearch_btn.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)

        self.race_teamscrollbar = ttk.Scrollbar(self.race_team_info_frame, )
        self.race_teamscrollbar.pack(side = 'right', fill = 'y')
        # 设置一个TreeViewUtils布局，用于显示比赛项目信息，列名：比赛ID、时间、地点、比赛名称、比赛类型，并插入到notebook中
        self.race_team_tree = RaceTeamTreeview(self.race_team_info_frame)
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.race_teamscrollbar.config(command = self.race_team_tree.yview)
        self.race_team_tree.configure(yscrollcommand = self.race_teamscrollbar.set)
        self.notebook.add(self.race_team_info_frame, text = "参赛队伍信息")
        self.race_teamscrollbar.config(command = self.race_team_tree.yview)


        # 各个项目奖牌信息
        self.medal_race_info_frame = ttk.Frame(self.notebook)
        self.medal_race_info_frame.pack(expand = True, fill = "both")
        medal_race_searchFrame = ttk.Frame(self.medal_race_info_frame)
        medal_race_searchFrame.pack(side = "top", fill = "x", expand = True)
        ttk.Label(medal_race_searchFrame, text = "队员搜索", font = ('Helvetica', 16)).pack(side = "left")
        self.medal_raceSearch_entry = ttk.Entry(medal_race_searchFrame, width = 80)
        self.medal_raceSearch_entry.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)
        self.medal_raceSearch_btn = ttk.Button(medal_race_searchFrame, text = "搜索")
        self.medal_raceSearch_btn.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5)

        self.medal_racescrollbar = ttk.Scrollbar(self.medal_race_info_frame, )
        self.medal_racescrollbar.pack(side = 'right', fill = 'y')
        # 设置一个TreeViewUtils布局，用于显示比赛项目信息，列名：比赛ID、时间、地点、比赛名称、比赛类型，并插入到notebook中
        self.medal_race_tree = MedalRaceInfoTreeview(self.medal_race_info_frame)
        # self.race_infoFrame.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.medal_racescrollbar.config(command = self.medal_race_tree.yview)
        self.medal_race_tree.configure(yscrollcommand = self.medal_racescrollbar.set)
        self.notebook.add(self.medal_race_info_frame, text = "参赛队伍信息")
        self.medal_racescrollbar.config(command = self.medal_race_tree.yview)

