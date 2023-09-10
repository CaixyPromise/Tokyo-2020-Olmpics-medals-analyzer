import concurrent.futures

from response.medal import MedalInsertResponse
from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter import messagebox
from services.Admins.Admin import AdminService
from models.competition import Competition
from models.team import NationalTeam
from models.medal_Rank import Medal_rank
from models.Users import User
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename
from utils.ExcelUtils import MakeTemplate, ReadTemplate
from models.enums import Column
from response.User import UserDeleteResponse, UserAddAdminResponse, UserModifyResponse
import difflib
from tkinter import StringVar

from utils.upload_file import copy_and_rename_files


class RaceButtonCommand(Ui_Function):
    question_config = {
        '比赛ID':   {'type': 'text'},
        '比赛时间': {'type': 'time'},
        '比赛大项': {'type': 'text'},
        '比赛名称': {'type': 'text'},
        '比赛地点': {'type': 'text'},
        '比赛类型': {'type': 'text'},
        '比赛状态': {'type': 'combobox', 'value': ('未开始', '已完成')},
        }

    def __init__(self, parent=None, **kwargs):
        super(RaceButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增比赛')
        win.wait_window()
        if win.result:
            race_node = Competition(*win.result)
            # # 提交数据库
            try:
                self.__service.insert_match(race_node)
            except Exception:
                messagebox.showinfo('提示', '添加失败, 比赛ID重复')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(race_node)
            self.main_tree.update()
            self.main_tree.insert_single(race_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')
    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]
            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_match(_id)
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))
        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                selection_node = Competition(*all_data)
                self.__service.modify_match(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

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

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.race.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, Competition)
            self.__service.insert_matchmany(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加比赛模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.race.value, filename)
            writer.make()


class TeamButtonCommand(Ui_Function):
    question_config = {
        '国家代码':   {'type': 'text'},
        '国家名称': {'type': 'text'},
        '团队总人数': {'type': 'text'},
        '管理员名称': {'type': 'text'},
        '管理员联系方式': {'type': 'text'},
        '管理员身份': {'type': 'text'},
        }
    def __init__(self, parent = None, **kwargs):
        super(TeamButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的


    def add(self, **kwags):
        # 新增队伍
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增国家队'
                                    )
        win.wait_window()
        if win.result:
            team_node = NationalTeam(*win.result)
            # # 提交数据库
            try:
                self.__service.insert_team(team_node)
                self.__service.insert_coutryAdmin(coutryID = NationalTeam.country_code, contact = NationalTeam.manager_contact)
            except Exception:
                messagebox.showinfo('提示', '添加失败')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(team_node)
            self.main_tree.update()
            self.main_tree.insert_single(team_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')

    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData(ret_type = 'all', value_type = 'text')

        if (selection is not None):
            _id = selection[1]

            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_team(_id)
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                coutry_code = self.treeview.item(item, 'text')
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                all_data.insert(0, coutry_code)
                selection_node = NationalTeam(*([coutry_code] + all_data))
                self.__service.modify_team(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

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

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.team.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, NationalTeam)
            self.__service.insert_teammany(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加国家队模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.team.value, filename)
            writer.make()


class MedalButtonCommand(Ui_Function):

    def __init__(self, parent = None, **kwargs):
        super(MedalButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')  # 主界面的tree
        self.treeview = self.parent.treeview  # 子界面的tree -- mannager 界面里的
        self.__gold_var = StringVar(value = '')
        self.__silver_var = StringVar(value = '')
        self.__bronze_var = StringVar(value = '')

        self.question_config = {
        '比赛ID/名称' : {'type' : 'text'},
        '金牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(1)}
            ]},
        '银牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(2)}
            ]},
        '铜牌/国家代码': {'type':'multi-part',
                          'cols' : [
            {'type': 'text'},
            {'type': 'label', 'text': '运动员名称'},
            {'type': 'text'},
            {'type': 'button', 'text': '精彩时刻', 'command' : lambda : self.__choice__(3)}
            ]},
        }

    def __choice__(self, _cls):
        file_path = askopenfilename(filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")])
        if file_path:
            if (_cls == 1):
                self.__gold_var.set(file_path)
            elif (_cls == 2):
                self.__silver_var.set(file_path)
            elif (_cls == 3):
                self.__bronze_var.set(file_path)

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增奖牌信息'
                                    )
        win.wait_window()

        record_path = [self.__gold_var.get(), self.__silver_var.get(), self.__bronze_var.get()]

        if win.result and all(record_path):
            race_id =  win.result[0]
            gold_code, gold_player = win.result[1]
            silver_code, silver_player = win.result[2]
            bronze_code, bronze_player = win.result[3]
            try:
                m = MedalInsertResponse(race_id = race_id,
                                        gold_code = gold_code,
                                        gold_player = gold_player,
                                        silver_code = silver_code,
                                        silver_player = silver_player,
                                        bronze_code = bronze_code,
                                        bronze_player = bronze_player
                                        )
            except ValueError:
                messagebox.showinfo('提示', '添加失败, 请检查信息是否完整')
                return


            race_name = self.__service.update_medal(m)
            print(race_name)
            print(type(race_name))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(copy_and_rename_files, record_path, race_id, race_name,
                                [gold_player, silver_player, bronze_player]
                                )


        # medal_node = Medal_rank(*win.result)
            # medal_node.count = medal_node.gold + medal_node.silver + medal_node.bronze
            # # # 提交数据库
            # try:
            #     self.__service.insert_medal(medal_node)
            # except Exception:
            #     messagebox.showinfo('提示', '添加失败, 比赛ID重复')
            # messagebox.showinfo('提示', '添加成功')
            # self.treeview.insert_single(medal_node)
            # self.main_tree.update()
            # self.main_tree.insert_single(medal_node)
            # self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败, 请检查信息是否完整')


    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]
            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_match(_id)
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data, item = selection
            if (column_index == -1 or column_index == 5):
                showerror(title = '提示', message = '不能修改排名或总数')
                return
            coutry_code = self.treeview.item(item, 'text')

            question_name = ('国家/地区', '国家/地区代码', '金牌', '银牌', '铜牌')
            question_name = list(self.question_config.keys())[column_index]
            # 生成提问窗口
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()


            if (win.result is not None):
                all_data = [-1] + list(all_data) + [all_data]
                all_data[column_index] = win.result[0]
                selection_node = Medal_rank(*all_data)
                if (column_index in {2, 3, 4, 5}):
                    selection_node.count = selection_node.gold + selection_node.silver + selection_node.bronze
                self.__service.modify_medal(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

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


    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                    filetypes = [('Excel files', '*.xlsx')]
                                    )
        if (file_path):
            columns = Column.race.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, Competition)
            self.__service.insert_medal(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()


    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加比赛模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.race.value, filename)
            writer.make()


class AdminButtonCommand(Ui_Function):
    question_config = {
        '管理员账号': {'type': 'text'},
        '管理员名称': {'type': 'text'},
        '管理员联系方式': {'type': 'text'},
        }

    def __init__(self, parent = None, **kwargs):
        super(AdminButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config,
                                    name = '新增管理员用户'
                                    )
        win.wait_window()
        if win.result:
            username, public_userid, user_contact = win.result
            user_node = User(group_id = 'Admin',
                             username = username,
                             password_hash = '123456',
                             role = 0,
                             public_userid = public_userid,
                             user_contact = user_contact,
                             )
            # # 提交数据库
            try:
                self.__service.insert_Adminuser(user_node)
            except Exception:
                messagebox.showinfo('提示', '添加失败, ID重复')
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert_single(user_node)
            self.main_tree.update()
            self.main_tree.insert_single(user_node)
            self.main_tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')

    def remove(self, **kwags):
        selection = self.treeview.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[1][0]

            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_admin(UserDeleteResponse(_id))
                self.treeview.delete(selection[0])
                self.treeview.update()
                self.main_tree.delete(selection[0])
                self.main_tree.update()
        return

    def modify(self, **kwags):
        selection = self.treeview.get_choice_columnData(kwags.get('event', None))

        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            if (column_index == 0):
                showerror('不可修改', '不可修改 用户账号')
                return
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(part_dict = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                before = all_data
                index = before[column_index]
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                selection_node = UserModifyResponse(public_userid = all_data[0],
                                                    username = all_data[1],
                                                    user_contact = all_data[2],)
                self.__service.modify_admin(selection_node)
                self.treeview.item(item, values = all_data)
                self.main_tree.item(item, values = all_data)

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

    def manny(self, **kwags):
        file_path = askopenfilename(title = '选择 Excel 文件',
                                               filetypes = [('Excel files', '*.xlsx')]
                                               )
        if (file_path):
            columns = Column.admin.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, UserAddAdminResponse)
            self.__service.insert_mannyAdmin(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加管理员模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.admin.value, filename)
            writer.make()
