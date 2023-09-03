from tkinter.ttk import Treeview
from PIL import Image, ImageTk
import tkinter

class TreeViewUtils(Treeview):
    def __init__(self, parent,
                 columns=None,
                 custom_headings = None,
                 custom_columns = None,
                 column_width=100,
                 **args):
        Treeview.__init__(self, parent, columns=columns, **args)


        self.pack(fill='both', expand=True)

        if columns:
            for col in columns:
                if custom_columns is None or col not in custom_columns:  # 添加这个检查
                    self.column(col, width = column_width, anchor = 'center')
                    self.heading(col, text = col)

        if custom_columns:
            for col, col_dict in custom_columns.items():
                self.column(col, **col_dict)

        if custom_headings:
            for col, col_dict in custom_headings.items():
                self.heading(col, **col_dict)
    @property
    def get_selection_all(self):
        return self.selection()
    @property
    def get_selection(self):
        try:
            return self.selection()[0]
        except Exception:
            raise ValueError('没有选中任何元素')

    def get_choice_columnData(self, event = None):
        try:
            item = self.get_selection  # 获取选中的项
            col = self.identify_column(event.x)  # 获取鼠标点击的列
            # 从列ID中获取列名（例如，从 '#1' 提取 '1'）
            col = col.split('#')[-1]
            col = int(col) - 1  # Make sure col is an integer
            col_name = self.cget("columns")[col]  # 从列列表中获取列名
            # 获取该行该列的值
            value = self.item(item, "values")
            return value[col], col, value, item  # 回传双击的行 + 列的值，还有列的下标，最后返回全部数据
        except Exception as E:
            print(E)
            raise ValueError('没有选中任何元素')

    def get_choice_RowData(self, ret_type = 'values', value_type = 'values'):
        try:
            item = self.get_selection  # 获取选中的项
            value = self.item(item, value_type)
            if (ret_type == 'values'):
                return value
            elif (ret_type == 'item'):
                return item
            else:
                return (item, value)
        except Exception as E:
            raise ValueError('没有选中值')

    def config(self, item, value):
        self.config(item = item, value = value)

    def insert_data(self, values, parent = '', index = tkinter.END, item = None, **kwargs):
        self.insert(parent, index, item, values = values, **kwargs)

    def sort_tree(self, tree, col, reverse, func):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key = func, reverse = reverse)
        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command = lambda _col = col: self.sort_tree(tree, _col, not reverse, func))

    def delete_item(self, item):
        self.delete(item)

    def update_item(self, item, values):
        for i, value in enumerate(values):
            self.item(item, values = (value,))

    def search_item(self, values, index):
        for item in self.get_children():
            if self.item(item)["values"][index] == values:
                return item
        return None

    def bindEvent(self, event_name, func):
        self.bind(event_name, func)