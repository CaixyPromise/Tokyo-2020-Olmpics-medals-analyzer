from multiprocessing import Process
from tkinter import Toplevel
from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter.messagebox import showinfo, showerror, askyesno
from services.Players.Player import PlayerService
import difflib
from response.User import InsertPlayerResponse, UserConfig, UserDeleteResponse, UserModifyResponse
from response.sighUpRace import SignUpRace
from models.competition import Competition
from ui.MediaWindow.MediaWindow import MediaPlayerDialogWindow, open_window


class RaceMannageButtonCommand(Ui_Function):
    question_config = {
        '报名比赛': {'type': 'combobox'},
        }

    def __init__(self, parent = None, **kwargs):
        super(RaceMannageButtonCommand, self).__init__(parent, **kwargs)
        self.__service = PlayerService()
        self.main_tree = self.part.get('tree')  # 主界面的tree
        self.treeview = self.parent.treeview  # 子界面的tree -- mannager 界面里的
        self.user_config: UserConfig = self.part.get('user_config')

    def add(self, **kwags):
        no_start_race = self.__service.query_race_with_status()
        race_dict = {
            i.competition_name: i.competition_id for i in no_start_race
            }
        self.question_config['报名比赛'] = {'type': 'combobox', 'value': [i.competition_name for i in no_start_race]}

        win = AskUserQuestionDialog(part_dict = self.question_config, name = '报名比赛')
        win.wait_window()
        if win.result:
            user_choice = win.result
            race_id = race_dict[user_choice[0]]
            user_node = SignUpRace(player_id = self.user_config.username,
                                   race_id = race_id,)
            # # 提交数据库
            try:
                race_info = self.__service.insert_race_sighup(user_node)
            except Exception as E:
                showinfo('提示', '报名失败！重复报名！')
                return
            showinfo('提示', '报名成功！！')
            race_node = Competition(*race_info)
            self.treeview.insert_single(race_node)
            self.main_tree.update()
            self.main_tree.insert_single(race_node)
            self.main_tree.update()
        else:
            showinfo('提示', '添加失败')

    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]

            if (askyesno('确认', '确定删除？')):
                self.__service.delete_race_sighup(UserDeleteResponse(_id))
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def search(self, ):
        target_string = self.parent.search_entry.get()
        if (target_string == ''):
            showerror('错误', '请输入搜索内容')
            return
        max_similarity = 0
        most_similar_item = None

        for item in self.treeview.get_children():
            row_data = self.treeview.item(item, "values")
            for cell_data in row_data:
                similarity = difflib.SequenceMatcher(None, target_string, cell_data).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_item = item

        if most_similar_item:
            self.treeview.selection_set(most_similar_item)
            self.treeview.see(most_similar_item)
        else:
            showerror('没有找到', '没有找到与输入相似的项')

class RewardMannageButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(RewardMannageButtonCommand, self).__init__(parent, **kwargs)
        self.__service = PlayerService()
        self.main_tree = self.part.get('tree')  # 主界面的tree
        self.treeview = self.parent.treeview  # 子界面的tree -- mannager 界面里的
        self.user_config: UserConfig = self.part.get('user_config')
        self.data = kwargs.get('data_node')
        self.parent_self = self.part.get('parent_self')

    def play(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            race_id, race_name = all_data
            video_path = f'static/reward/{race_id}_{race_name}_{self.user_config.public_userid}'
            # top_win = Toplevel(self.parent_self)
            # w = MediaPlayerDialogWindow(top_win, video_path)
            title = f'{self.user_config.username}-{race_name}_精彩时刻'
            p = Process(target = open_window, args = (video_path, title))
            p.start()
