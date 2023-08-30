from ui.AdminWindow import AdminDialogWindow
from typing import List, Optional
from response.rank import MedalRankData
from services.medal_rank import MedalRankService
from utils.make_image import make_image
import tkinter as tk
class AdminWindow(AdminDialogWindow):

    def add_image2Attr(self, name, image):
        setattr(self, name, make_image(image))
    def setup_image(self, Node : List[MedalRankData]):
        [self.add_image2Attr(val.countryid, val.flag) for val in Node]

    def __init__(self, master, UserInfo, **kwargs):
        super().__init__(master, **kwargs)
        self.get_db()
        self.init_medalRank()

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
        self.__rank_db = MedalRankService()
        # 获取奖牌榜
        self.__medal_rank = self.__rank_db.query_all_rank()
        self.setup_image(self.__medal_rank)

        # 根据奖牌榜排序获取金牌榜
        self.__gold_rank = self.init_glodRank(self.__rank_db.query_all_rank())

    def init_medalRank(self):
        result = self.__medal_rank
        for medal_node, gold_node in zip(self.__medal_rank, self.__gold_rank):
            self.MedalRank_tree.insert('', tk.END,
                                      text = (medal_node.rank),
                                      image = getattr(self, medal_node.countryid),
                                      values = (medal_node.countryname,
                                             medal_node.gold,
                                             medal_node.silver,
                                             medal_node.bronze,
                                             medal_node.count)
                                      )
            self.goldRank_tree.insert('', tk.END,
                                       text = (gold_node.rank),
                                       image = getattr(self, gold_node.countryid),
                                       values = (gold_node.countryname,
                                                 gold_node.gold,
                                                 gold_node.silver,
                                                 gold_node.bronze,
                                                 gold_node.count))
        # self.setup_image(self.__medal_rank.query_all_rank())