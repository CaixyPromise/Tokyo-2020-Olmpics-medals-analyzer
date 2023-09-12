import difflib
from tkinter.messagebox import showerror
from ui.TeamAdminWindow import TeamAdminDialogWindow
from utils.make_image import make_image
from services.TeamAdmins.TeamAdmin import TeamAdminService
from copy import deepcopy
import tkinter as tk
from ui.MannagerWindow import MannageDialogWindow
from models.enums import Column, ColumnName
from utils.GlobalStatic import GlobalResources
from ui.common.RankTreeview import RankTreeview
from ui.common.RaceTreeview import RaceTreeview
from ui.common.TeamTreeview import TeamTreeview
from ui.common.UserTreeview import UserTreeview
from tkinter import Toplevel
from services.TeamAdmins.command import InsertPlalyerButtonCommand

class TeamAdminWindow(TeamAdminDialogWindow):
    def __init__(self, parent, UserInfo, **kwargs):
        super(TeamAdminWindow, self).__init__(parent)
        self.__db = TeamAdminService()
        self.__static = GlobalResources()
        self.__user_config = self.__static['user_config']
        self.get_db()
        self.init_medalRank()
        self.bind_function()
        self.init_button_function()



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

    def search(self, search_entry, treeview, column_index = None):
        target_string = search_entry
        if target_string == '':
            showerror('错误', '请输入搜索内容')
            return

        max_similarity = 0
        most_similar_item = None

        for item in treeview.get_children():
            row_data = treeview.item(item, "values")
            if (column_index):
                # 只在 国家名称 和 国家代码 列进行搜索
                search_columns = [row_data[i] for i in column_index]
            else:
                search_columns = row_data

            for cell_data in search_columns:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            treeview.selection_set(most_similar_item)
            treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')

    def bind_search_function(self, button, entry, tree):
        button.config(command = lambda: self.search(entry.get().upper(), tree))
        entry.bind('<Return>', lambda x: self.search(entry.get().upper(), tree))

    def bind_function(self):
        self.bind_search_function(self.goldRankSearch_button, self.goldRankSearch_entry, self.goldRank_tree)
        self.bind_search_function(self.medalRankSearch_btn, self.medalRankSearch_entry, self.medalRank_tree)
        self.bind_search_function(self.countryRankSearch_btn, self.countryRankSearch_entry, self.country_tree)
        self.bind_search_function(self.race_teamSearch_btn, self.race_teamSearch_entry, self.race_team_tree)

    def setup_DialogWindow(self, data, function):

        win = Toplevel(self)
        dialog = MannageDialogWindow(win, app_name = function,)
        match function:
            case ColumnName.country_admin:
                dialog.setup_ui(UserTreeview, init_data = data)
                Button_event = InsertPlalyerButtonCommand(dialog,
                                      tree = self.race_tree,
                                      user_config = self.__static['user_config'])
            case _:
                Button_event = None

        dialog.setup_func(Button_event)
        dialog.pack()
        dialog.mainloop()

    def init_button_function(self):
        self.race_mannageBtn.config(command = lambda : self.setup_DialogWindow(self.__db.query_user_by_id(
                self.__user_config.group_id),
                ColumnName.country_admin))
        self.exit_sysBtn.config(command = lambda : [exit(0)])

    def get_db(self):
        # 获取奖牌榜
        self.__medal_rank = self.__db.query_medal_rank()
        self.__static['flags'] = {val.countryid: make_image(val.flag) for val in self.__medal_rank}
        # 根据奖牌榜排序获取金牌榜 --> 深拷贝
        self.__gold_rank = self.init_glodRank(deepcopy(self.__medal_rank))

    def init_medalRank(self):
        result = self.__medal_rank
        self.medalRank_tree.insert_manny(self.__medal_rank)
        self.goldRank_tree.insert_manny(self.__gold_rank)
        self.race_tree.insert_manny(self.__db.query_all_race())
        self.country_tree.insert_manny(self.__db.query_user_by_id(
                self.__user_config.group_id))
        self.race_team_tree.insert_manny(self.__db.query_race_team())
