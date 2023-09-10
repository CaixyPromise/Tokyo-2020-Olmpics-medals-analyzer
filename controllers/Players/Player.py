import difflib
from tkinter.messagebox import showerror
from ui.PlayerWindow import PlayerDialogWindow
from ui.common.RewardTreeview import RewardTreeview
from utils.make_image import make_image
from services.Players.Player import PlayerService
from copy import deepcopy
import tkinter as tk
from ui.MannagerWindow import MannageDialogWindow
from models.enums import ColumnName
from utils.GlobalStatic import GlobalResources
from ui.common.RaceTreeview import RaceTreeview
from ui.common.UserTreeview import UserTreeview
from tkinter import Toplevel
from services.Players.command import RaceMannageButtonCommand

class PlayerWindow(PlayerDialogWindow):
    def __init__(self, parent, UserInfo, **kwargs):
        super(PlayerWindow, self).__init__(parent)
        self.__db = PlayerService()
        self.__static = GlobalResources()
        self.__User = UserInfo
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

    def bind_function(self):
        self.goldRankSearch_button.config(command = lambda : self.search(self.goldRankSearch_entry.get().upper(),
                                                                         self.goldRank_tree,
                                                                         column_index = (0, 1)),)
        self.medalRankSearch_btn.config(command = lambda : self.search(self.medalRankSearch_entry.get().upper(),
                                                                       self.medalRank_tree,
                                                                         column_index = (0, 1)))
        self.raceRankSearch_btn.config(command = lambda : self.search(self.raceRankSearch_entry.get().upper(),
                                                                      self.race_tree,
                                                                         column_index = (0, 2, 3, 4)))
        self.goldRankSearch_entry.bind('<Return>', lambda x:self.search(self.goldRankSearch_entry.get().upper(),
                                                                         self.goldRank_tree,
                                                                         column_index = (0, 1)))
        self.medalRankSearch_entry.bind('<Return>', lambda x : self.search(self.medalRankSearch_entry.get().upper(),
                                                                       self.medalRank_tree,
                                                                         column_index = (0, 1)))
        self.raceRankSearch_entry.bind('<Return>', lambda x:self.search(self.raceRankSearch_entry.get().upper(),
                                                                      self.race_tree,
                                                                         column_index = (0, 2, 3, 4)))

    def setup_DialogWindow(self, data, function):
        ret_val = tk.Variable()

        win = Toplevel(self)
        dialog = MannageDialogWindow(win, app_name = function, )
        match function:
            case ColumnName.player:
                dialog.setup_ui(RaceTreeview, init_data = data)
                Button_event = RaceMannageButtonCommand(dialog,
                                                        tree = self.play_race_tree,
                                                        user_config = self.__static['user_config'])
            case ColumnName.reward:
                dialog.setup_ui(RewardTreeview, init_data = data, init_command = False)
                Button_event = RewardMannageButtonCommand(dialog,
            case _:
                Button_event = None

        dialog.setup_func(Button_event, all_ = False)
        dialog.pack()
        dialog.mainloop()

    def init_button_function(self):
        self.race_mannageBtn.config(
            command = lambda: self.setup_DialogWindow(
                    self.__db.query_race_by_playID(self.__User.username),
                    ColumnName.player
                    )
                )
        self.exit_systemBTN.config(command = lambda: [exit(0)])
        self.reward_mannageBtn.config(
                command = lambda: self.setup_DialogWindow(
                        self.__db.query_reward_by_playID(self.__User.username),
                        ColumnName.reward
                        )
                )

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
        self.play_race_tree.insert_manny(self.__db.query_race_by_playID(self.__User.username))