from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter.messagebox import showinfo, showerror, askyesno
from services.TeamAdmins.TeamAdmin import TeamAdminService
import difflib
from tkinter.filedialog import askopenfilename, asksaveasfilename
from models.enums import Column
from utils.ExcelUtils import ReadTemplate, MakeTemplate
from response.User import InsertPlayerResponse, UserConfig, UserDeleteResponse, UserModifyResponse

class InsertPlalyerButtonCommand(Ui_Function):
    question_config = {
        '运动员账号': {'type': 'text'},
        '运动员名称': {'type': 'text'},
        '运动员联系方式': {'type': 'text'},
        }

    def __init__(self, parent = None, **kwargs):
        super(InsertPlalyerButtonCommand, self).__init__(parent, **kwargs)
        self.__service = TeamAdminService()
        self.main_tree = self.part.get('tree')       # 主界面的tree
        self.treeview = self.parent.treeview         # 子界面的tree -- mannager 界面里的
        self.user_config : UserConfig = self.part.get('user_config')

    def add(self, **kwags):
        win = AskUserQuestionDialog(part_dict = self.question_config, name = '新增运动员')
        win.wait_window()
        if win.result:
            username, public_userid, user_contact = win.result
            user_node = InsertPlayerResponse(group_id = self.user_config.group_id,
                             username = username,
                             password_hash = '123456',
                             role = 2,
                             public_userid = public_userid,
                             user_contact = user_contact,
                             )
            # # 提交数据库
            try:
                self.__service.insert_player(user_node)
            except Exception:
                showinfo('提示', '添加失败, 用户重复')
            showinfo('提示', '添加成功，使用用户名称登陆！密码默认为123456')
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
                self.__service.delete_player(UserDeleteResponse(_id))
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
                                                    user_contact = all_data[2])
                self.__service.modify_player(selection_node)
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
            columns = Column.player.value
            reader = ReadTemplate(file_path)
            data = reader.read(columns, InsertPlayerResponse)
            self.__service.insert_manny_player(data)
            self.treeview.insert_manny(data)
            self.main_tree.update()
            self.main_tree.insert_manny(data)
            self.main_tree.update()

    def template(self):
        options = {
            'defaultextension': '.xlsx',
            'filetypes':        [('Excel files', '.xlsx'), ('All files', '.*')],
            'initialfile':      '批量添加运动员模板.xlsx',
            'title':            '选择保存位置'
            }
        filename = asksaveasfilename(**options)
        if (filename):
            writer = MakeTemplate(Column.player.value, filename)
            writer.make()