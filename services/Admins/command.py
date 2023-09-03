from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter import messagebox
from services.Admins.Admin import AdminService
from models.competition import Competition
from models.team import NationalTeam
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfilename, askopenfilename
from utils.ExcelUtils import MakeTemplate, ReadTemplate
from models.enums import Column
import difflib

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
        win = AskUserQuestionDialog(columns = self.question_config,
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
        print(f"selection: {selection}")
        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(columns = column,
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
        win = AskUserQuestionDialog(columns = self.question_config,
                                    name = '新增国家队'
                                    )
        win.wait_window()
        if win.result:
            team_node = NationalTeam(*win.result)
            # # 提交数据库
            try:
                self.__service.insert_team(team_node)
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
        print(selection)
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
        print(f"selection: {selection}")
        if (selection is not None):
            # 双击行列的值  值的下标       整行的数据  item
            column_data, column_index, all_data,  item = selection
            question_name = list(self.question_config.keys())[column_index]
            column = {question_name: self.question_config[question_name]}
            win = AskUserQuestionDialog(columns = column,
                                        name = f'修改 {question_name}')
            win.wait_window()
            if (win.result is not None):
                coutry_code = self.treeview.item(item, 'text')
                all_data = list(all_data)
                all_data[column_index] = win.result[0]
                all_data.insert(0, coutry_code)
                selection_node = NationalTeam(*all_data)
                self.__service.modify_team(selection_node)
                del all_data[0]
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
    question_config = {
        '排名':   {'type': 'text'},
        '比赛时间': {'type': 'time'},
        '比赛大项': {'type': 'text'},
        '比赛名称': {'type': 'text'},
        '比赛地点': {'type': 'text'},
        '比赛类型': {'type': 'text'},
        '比赛状态': {'type': 'combobox', 'value': ('未开始', '已完成')},
        }
    def __init__(self, parent = None, **kwargs):
        super(MedalButtonCommand, self).__init__(parent, **kwargs)

    def add(self, **kwags):
        pass

    def remove(self, **kwags):
        pass

    def modify(self, **kwags):
        pass

    def manny(self, **kwags):
        pass


class AdminButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(AdminButtonCommand, self).__init__(parent, **kwargs)

    def add(self, **kwags):
        win = AskUserQuestionDialog(columns = self.part.get('columns'),
                                    name = '新增比赛'
                                    )
        win.wait_window()
        if win.result:
            # 提交数据库
            pass

    def remove(self, **kwags):
        tree = self.part.get('tree')
        selected_rows = tree.selection() # 获取选中的行
        if not selected_rows:  # 如果没有选中的行，直接返回
            return
        # 弹出确认对话框
        confirm = messagebox.askyesno("确认", "你确定要删除选中的行吗？")
        if confirm:
            for row in selected_rows:
                tree.delete(row)  # 删除选中的行

    def modify(self, **kwags):
        treeview = self.part.get('tree')
        item = treeview.selection()[0]  # 获取选中的项
        col = treeview.identify_column(event.x)  # 获取鼠标点击的列

        # 从列ID中获取列名（例如，从 '#1' 提取 '1'）
        col = col.split('#')[-1]
        col = int(col) - 1
        col = treeview.cget("columns")[col]  # 从列列表中获取列名

        # 获取该行该列的值
        value = treeview.item(item, "values")[col]
        entry = self.part.get('entry')
        entry.delete(0, 'end')
        entry.insert(0, value)

    def manny(self, **kwags):
        pass