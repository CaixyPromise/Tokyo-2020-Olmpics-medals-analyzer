from ui.AdminWindow import AdminDialogWindow
from typing import List
from response.rank import MedalRankData
from services.medal_rank import MedalRankService
from utils.make_image import make_image
import tkinter as tk
from ui.MannagerWindow import MannageDialogWindow
from tkinter import Toplevel
from models.enums import Column, ColumnName
from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from services.Admin import AdminService
from copy import deepcopy
# class ButtonFunction(Ui_Function):
#     def __init__(self, parent):
#         super(ButtonFunction, self).__init__()
#         self.ret_val = tk.Variable()
#         self.parent = parent
#
#     @staticmethod
#     def on_item_double_click(event, treeview):
#         item = treeview.selection()[0]  # 获取选中的项
#         col = treeview.identify_column(event.x)  # 获取鼠标点击的列
#
#         # 从列ID中获取列名（例如，从 '#1' 提取 '1'）
#         col = col.split('#')[-1]
#         col = int(col) - 1
#         col = treeview.cget("columns")[col]  # 从列列表中获取列名
#
#         # 获取该行该列的值
#         value = treeview.item(item, "values")[col]
#
#
#     def setup_team(self):
#         def add():
#             win = AskUserQuestionDialog(columns = Column.team.value,
#                                         name = '新增国家队管理员', return_val = self.ret_val)
#             win.wait_window()
#
#         def edit():
#             pass
#
#         def delete():
#             pass
#
#         def search():
#             pass
#
#         def reset():
#             pass



class AdminWindow(AdminDialogWindow):

    def add_image2Attr(self, name, image):
        setattr(self, name, make_image(image))

    def setup_image(self, Node : List[MedalRankData]):
        [self.add_image2Attr(val.countryid, val.flag) for val in Node]

    def __init__(self, master, UserInfo, **kwargs):
        super().__init__(master, **kwargs)
        self.__db = AdminService()
        self.get_db()
        self.init_medalRank()
        self.init_button_function()


    def get_treeInfo(self, event, treeview):
        item = treeview.selection()[0]  # 获取选中的项
        col = treeview.identify_column(event.x)  # 获取鼠标点击的列

        # 从列ID中获取列名（例如，从 '#1' 提取 '1'）
        col = col.split('#')[-1]
        col = int(col) - 1
        col = treeview.cget("columns")[col]  # 从列列表中获取列名

        # 获取该行该列的值
        value = treeview.item(item, "values")[col]

    def setup_DialogWindow(self, columns, function):
        ret_val = tk.Variable()
        def add():
            add_win = AskUserQuestionDialog(columns = Column.team.value,
                                            name = '新增国家队管理员', return_val = ret_val)
            add_win.wait_window()


        def edit(event, treeview):
            item = treeview.selection()[0]  # 获取选中的项
            col = treeview.identify_column(event.x)  # 获取鼠标点击的列

            # 从列ID中获取列名（例如，从 '#1' 提取 '1'）
            col = col.split('#')[-1]
            col = int(col) - 1
            col = treeview.cget("columns")[col]  # 从列列表中获取列名

            # 获取该行该列的值
            value = treeview.item(item, "values")[col]

        def delete():
            pass

        def search():
            pass


        # Button_event = ButtonFunction(self)
        #
        # win = Toplevel(self)
        # dialog = MannageDialogWindow(win,
        #                              columns =  columns,
        #                              app_name = function,
        #                              function_tool = Button_event
        #                              )
        #
        # dialog.pack()
        # dialog.mainloop()

    def init_button_function(self):

        self.race_mannageBtn.config(command = lambda : self.setup_DialogWindow(Column.race, ColumnName.race))
        self.team_mannageBtn.config(command = lambda : self.setup_DialogWindow(Column.team, ColumnName.team))
        self.medal_mannageBtn.config(command = lambda : self.setup_DialogWindow(Column.medal, ColumnName.medal))
        self.admin_mannageBtn.config(command = lambda : self.setup_DialogWindow(Column.admin, ColumnName.admin))

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
        self.setup_image(self.__medal_rank)
        # 根据奖牌榜排序获取金牌榜 --> 深拷贝
        self.__gold_rank = self.init_glodRank(deepcopy(self.__medal_rank))

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