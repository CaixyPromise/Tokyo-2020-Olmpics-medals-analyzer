import tkinter.ttk as ttk
import tkinter as tk
from ui.utils.TreeviewUtils import TreeViewUtils
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from utils.make_image import make_image
from tkinter.messagebox import showerror

class MannageDialogWindow(ttk.Frame):
    def __init__(self, parent, columns, app_name, init_data = None, **kwargs):
        super(MannageDialogWindow, self).__init__(parent, **kwargs)
        self.parent = parent
        self.columns = columns.value
        self.app = app_name.value
        self.__tree_data =  init_data
        self.setup_ui()

    def setup_func(self, function):
        """
        TODO: 根据传入的app身份参数，绑定特定的函数
        :return:
        """
        self.function = function
        self.add_button.config(command =  self.function.add)
        self.delete_button.config(command = self.function.remove)
        self.modify_button.config(command = self.function.modify)
        self.BacthAdd_button.config(command = self.function.manny)
    def get_choice_columnDataByrow(self, event = None):
        try:
            return self.treeview.get_choice_columnDataByrow()
        except Exception as E:
            print(E)
            showerror('没有选中值', '请先在左侧选中值')

    def get_choice_RowData(self, ret_type = 'values'):
        try:
            return self.treeview.get_choice_RowData(ret_type)
        except Exception as E:
            print(E)
            showerror('没有选中值', '请先在左侧选中值')

    def setup_ui(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", expand=True)
        self.treeview = TreeViewUtils(left_frame, columns = self.columns,
                                      show = 'headings')
        right_frame = ttk.Frame(self)
        right_frame.pack(side="right", fill="y", expand=True)
        self.add_button = ttk.Button(right_frame, text=f"添加{self.app}")
        self.add_button.pack(padx = (10, 10), pady = (10, 10))

        self.BacthAdd_button = ttk.Button(right_frame, text = f"批量添加{self.app}")
        self.BacthAdd_button.pack(padx = (10, 10), pady = (10, 10))

        self.modify_button = ttk.Button(right_frame, text= f"修改{self.app}")
        self.modify_button.pack(padx = (10, 10), pady = (10, 10))

        self.delete_button = ttk.Button(right_frame, text=f"删除{self.app}")
        self.delete_button.pack(padx = (10, 10), pady = (10, 10))
        
        self.search_button = ttk.Button(right_frame, text=f"查找{self.app}")
        self.search_button.pack(padx = (10, 10), pady = (10, 10))
        self.search_entry = ttk.Entry(right_frame)
        self.search_entry.pack(padx = (10, 10), pady = (10, 10))

        self.submit_button = ttk.Button(right_frame, text=f"提交更改")
        self.submit_button.pack(padx = (10, 10), pady = (10, 10))

        self.cancel_button = ttk.Button(right_frame, text=f"取消更改")
        self.cancel_button.pack(padx = (10, 10), pady = (10, 10))

        if (self.__tree_data):
            for race_node in self.__tree_data:
                self.treeview.insert('', 'end', values = (race_node.competition_id,
                                                          race_node.time,
                                                  race_node.main_event,
                                                  race_node.competition_name,
                                                  race_node.venue,
                                                  race_node.competition_type,
                                                  race_node.status))

