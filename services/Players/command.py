from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter.messagebox import showinfo, showerror, askyesno
from services.Players.Player import PlayerService
import difflib
from tkinter.filedialog import askopenfilename, asksaveasfilename
from models.enums import Column
from utils.ExcelUtils import ReadTemplate, MakeTemplate
from response.User import InsertPlayerResponse, UserConfig, UserDeleteResponse, UserModifyResponse
from response.sighUpRaceResponse import SignUpRace

class RaceMannageButtonCommand(Ui_Function):
    question_config = {
        '比赛状态': {'type': 'combobox'},
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
        self.question_config.update('比赛状态', {'type': 'combobox', 'values': [i.competition_name for i in no_start_race]})
        win = AskUserQuestionDialog(columns = self.question_config, name = '报名比赛')
        win.wait_window()
        if win.result:
            user_choice = win.result
            race_id = race_dict[user_choice]
            user_node = SignUpRace(player_id = self.user_config.username,
                                   race_id = race_id,)
            # # 提交数据库
            try:
                self.__service.insert_race_sighup(user_node)
            except Exception:
                showinfo('提示', '报名失败！重复报名！')
            showinfo('提示', '报名成功！！')
            self.treeview.insert_single(user_node)
            self.main_tree.update()
            self.main_tree.insert_single(user_node)
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