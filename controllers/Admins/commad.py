from ui.utils.functions import Ui_Function
from ui.AskUserQuestionWindow import AskUserQuestionDialog
from tkinter import messagebox

class RaceButtonCommand(Ui_Function):
    def __init__(self, parent=None, **kwargs):
        super(RaceButtonCommand, self).__init__(parent, **kwargs)

    def add(self):
        win = AskUserQuestionDialog(columns = self.part.get('columns'),
                                    name = '新增比赛')
        win.wait_window()
        if win.result:
            # 提交数据库
            pass


    def remove(self):
        pass

    def edit(self):
        pass

    def manny(self):
        pass


class TeamButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(TeamButtonCommand, self).__init__(parent, **kwargs)

    def add(self):
        win = AskUserQuestionDialog(columns = self.part.get('columns'),
                                    name = '新增队伍'
                                    )
        win.wait_window()
        if win.result:
            # 提交数据库
            pass

    def remove(self):
        pass

    def edit(self):
        pass

    def manny(self):
        pass


class MedalButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(MedalButtonCommand, self).__init__(parent, **kwargs)

    def add(self):
        pass

    def remove(self):
        pass

    def edit(self):
        pass

    def manny(self):
        pass


class AdminButtonCommand(Ui_Function):
    def __init__(self, parent = None, **kwargs):
        super(AdminButtonCommand, self).__init__(parent, **kwargs)

    def add(self):
        win = AskUserQuestionDialog(columns = self.part.get('columns'),
                                    name = '新增比赛'
                                    )
        win.wait_window()
        if win.result:
            # 提交数据库
            pass

    def remove(self):
        tree = self.part.get('tree')
        selected_rows = tree.selection() # 获取选中的行
        if not selected_rows:  # 如果没有选中的行，直接返回
            return
        # 弹出确认对话框
        confirm = messagebox.askyesno("确认", "你确定要删除选中的行吗？")
        if confirm:
            for row in selected_rows:
                tree.delete(row)  # 删除选中的行

    def edit(self, event = None):
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

    def manny(self):
        pass