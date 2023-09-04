from ui.AdminWindow import AdminDialogWindow
from utils.make_image import make_image
import tkinter as tk
from models.enums import ColumnName
from services.Admins.Admin import AdminService
from copy import deepcopy
from tkinter import Toplevel
from ui.MannagerWindow import MannageDialogWindow
from services.Admins.command import RaceButtonCommand, TeamButtonCommand, MedalButtonCommand, AdminButtonCommand
from utils.GlobalStatic import GlobalResources
from ui.common.RankTreeview import RankTreeview
from ui.common.RaceTreeview import RaceTreeview
from ui.common.TeamTreeview import TeamTreeview
from ui.common.AdminTreeview import AdminTreeview

class AdminWindow(AdminDialogWindow):
    def __init__(self, master, UserInfo, **kwargs):
        super().__init__(master, **kwargs)
        self.__db = AdminService()
        self.__static = GlobalResources()
        self.get_db()
        self.init_medalRank()
        self.init_button_function()

    def setup_DialogWindow(self, data, function):
        ret_val = tk.Variable()

        win = Toplevel(self)
        dialog = MannageDialogWindow(win, app_name = function,)
        match function:
            case ColumnName.race:
                dialog.setup_ui(RaceTreeview, init_data = data)
                Button_event = RaceButtonCommand(dialog, tree = self.race_tree)
            case ColumnName.team:
                dialog.setup_ui(TeamTreeview, init_data = data)
                Button_event = TeamButtonCommand(dialog, tree = self.team_tree)
            case ColumnName.medal:
                dialog.setup_ui(RankTreeview, init_data = data)
                Button_event = MedalButtonCommand(dialog, tree = self.medalRank_tree)
            case ColumnName.admin:
                dialog.setup_ui(AdminTreeview, init_data = data)
                Button_event = AdminButtonCommand(dialog, tree = self.admin_tree)
            case _:
                Button_event = None

        dialog.setup_func(Button_event)
        dialog.pack()
        dialog.mainloop()

    def init_button_function(self):
        self.race_mannageBtn.config(command = lambda : self.setup_DialogWindow(self.__db.query_all_race(), ColumnName.race))
        self.team_mannageBtn.config(command = lambda : self.setup_DialogWindow(self.__db.query_all_team(), ColumnName.team))
        self.medal_mannageBtn.config(command = lambda : self.setup_DialogWindow(self.__db.query_medal_rank(), ColumnName.medal))
        self.admin_mannageBtn.config(command = lambda : self.setup_DialogWindow(self.__db.query_admin(), ColumnName.admin))

    @staticmethod
    def init_glodRank(medal_rank):
        # 排序金牌榜，优先排金牌，其次排总数
        # 如果金牌相同，再比较总数区分顺序
        sorted_gold_rank = sorted(medal_rank, key = lambda x: (x.gold, x.count), reverse = True)

        # 初始化排名和上一个金牌数和总数
        current_rank = 0
        last_gold = None
        last_count = None
        num_tied = 1  # 用于追踪并列的数量

        # 遍历排序后的列表来设置排名
        # 金牌/奖牌数 相同则国家并列，但是到下一个金牌数的下一位应该要算上并列的排名。
        for item in sorted_gold_rank:
            if last_gold == item.gold and last_count == item.count:
                # 并列情况：保持当前排名不变，但增加并列数量
                item.rank = current_rank
                num_tied += 1
            else:
                # 不是并列情况：更新排名（考虑之前的并列数量）
                current_rank += num_tied
                item.rank = current_rank
                num_tied = 1  # 重置并列数量

            # 更新上一个金牌数和总数以便于下一次比较
            last_gold = item.gold
            last_count = item.count
        return sorted_gold_rank

    def get_db(self):
        # 获取奖牌榜
        self.__medal_rank = self.__db.query_medal_rank()
        self.__static['flags'] = {val.countryid : make_image(val.flag) for val in self.__medal_rank}
        # 根据奖牌榜排序获取金牌榜 --> 深拷贝
        self.__gold_rank = self.init_glodRank(deepcopy(self.__medal_rank))

    def init_medalRank(self):
        self.medalRank_tree.insert_manny(self.__medal_rank)
        self.goldRank_tree.insert_manny(self.__gold_rank)
        self.race_tree.insert_manny(self.__db.query_all_race())
        self.team_tree.insert_manny(self.__db.query_all_team())
        self.admin_tree.insert_manny(self.__db.query_admin())
