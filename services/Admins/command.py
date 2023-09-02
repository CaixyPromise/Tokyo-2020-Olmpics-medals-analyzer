from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter import messagebox
from services.Admins.Admin import AdminService
from models.competition import Competition

class RaceButtonCommand(Ui_Function):
    def __init__(self, parent=None, **kwargs):
        super(RaceButtonCommand, self).__init__(parent, **kwargs)
        self.__service = AdminService()
        self.tree = self.part.get('tree')
        self.treeview = self.parent.treeview

    def add(self, **kwags):
        column = {
            '比赛ID' : {'type' : 'text'},
            '比赛时间' : {'type' : 'time'},
            '比赛大项' : {'type' : 'text'},
            '比赛名称': {'type': 'text'},
            '比赛地点': {'type': 'text'},
            '比赛类型': {'type': 'text'},
            '比赛状态': {'type': 'combobox', 'value' : ('未开始', '已完成')},
            }



        win = AskUserQuestionDialog(columns = column,
                                    name = '新增比赛')
        win.wait_window()
        if win.result:
            race_node = Competition(*win.result)
            # # 提交数据库
            self.__service.insert_match(race_node)
            messagebox.showinfo('提示', '添加成功')
            self.treeview.insert('', 'end', values = (race_node.time, race_node.venue,
                                                  race_node.competition_name,
                                                  race_node.competition_type,
                                                  race_node.status,)
                             )
            self.tree.update()
            self.tree.insert('', 'end', values=(race_node.time, race_node.venue,
                                                race_node.competition_name,
                                                race_node.competition_type,
                                                race_node.status))
            self.tree.update()
        else:
            messagebox.showinfo('提示', '添加失败')
    def remove(self, **kwags):
        selection = self.parent.get_choice_RowData('all')
        if (selection is not None):
            _id = selection[0]
            if (messagebox.askyesno('确认', '确定删除？')):
                self.__service.delete_match(_id)
            self.treeview.delete(selection[0])
            self.treeview.update()
        return

    def modify(self, **kwags):
        self.__service.modify_match(kwags.get('data'))

    def manny(self, **kwags):
        self.__service.insert_matchmany(kwags.get('data'))


class TeamButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(TeamButtonCommand, self).__init__(parent, **kwargs)

    def add(self, **kwags):
        # 新增队伍
        columns = {
            '国家名称' : 'text',
            '国家代码' : 'text',
            '总人数'   : 'text',
            }
        win = AskUserQuestionDialog(columns = self.part.get('columns'),
                                    name = '新增队伍'
                                    )
        win.wait_window()
        if win.result:
            # 提交数据库
            pass

    def remove(self, **kwags):
        pass

    def modify(self, **kwags):
        pass

    def manny(self, **kwags):
        pass


class MedalButtonCommand(Ui_Function):
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