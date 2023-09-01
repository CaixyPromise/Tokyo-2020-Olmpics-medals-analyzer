import tkinter.ttk as ttk
import tkinter as tk
from ui.utils.TreeviewUtils import TreeViewUtils
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from utils.make_image import make_image

class MannageDialogWindow(ttk.Frame):
    def __init__(self, parent, columns, app_name, function_tool, init_data = None, **kwargs):
        super(MannageDialogWindow, self).__init__(parent, **kwargs)
        self.parent = parent
        self.columns = columns.value
        self.app = app_name.value
        self.setup_ui()
        self.function = function_tool
        self.__tree_data =  init_data
        self.setup_func()

    def setup_func(self):
        """
        TODO: 根据传入的app身份参数，绑定特定的函数
        :return:
        """
        self.add_button.config(command =  self.function.add)
        self.delete_button.config(command = self.function.remove)
        self.modify_button.config(command = self.function.modify)
        self.BacthAdd_button.config(command = self.function.manny)


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
