# 增删查改的管理界面，根据传入参数渲染界面
import tkinter.ttk as ttk
import tkinter as tk
from ui.utils.TreeviewUtils import TreeViewUtils
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from utils.make_image import make_image
from tkinter.messagebox import showerror
from copy import deepcopy

class MannageDialogWindow(ttk.Frame):
    def __init__(self, parent,  app_name, headings = 'headings', init_data = None, **kwargs):
        super(MannageDialogWindow, self).__init__(parent, **kwargs)
        self.parent = parent
        self.app = app_name.value
        self.headings = headings

    def setup_func(self, function, all_ = True):
        self.function = function
        if (self.function is None):
            return
        if (all_ is True):
            self.add_button.config(command = self.function.add)
            self.delete_button.config(command = self.function.remove)
            self.treeview.bind('<Double-1>', lambda event: self.function.modify(event = event))
            self.search_button.config(command = self.function.search)
            self.BacthAdd_button.config(command = self.function.manny)
            self.template_button.config(command = self.function.template)
        elif (all_ == 'tree'):
            self.treeview.bind('<Double-1>', lambda event: self.function.play(event = event))
        else:
            self.add_button.config(command = self.function.add)
            self.delete_button.config(command = self.function.remove)
            self.treeview.bind('<Double-1>', lambda event: self.function.modify(event = event))
            self.search_button.config(command = self.function.search)



    def setup_ui(self, tree, init_data, init_command = True):
        left_frame = ttk.Frame(self)
        if (init_command):

            left_frame.pack(side="left", fill="y", expand=True)
        else:
            left_frame.pack(fill="both", expand=True)
        self.treeview = tree(left_frame)

        if (init_command):
            right_frame = ttk.Frame(self)
            right_frame.pack(side="right", fill="y", expand=True)
            self.add_button = ttk.Button(right_frame, text=f"添加{self.app}")
            self.add_button.pack(padx = (10, 10), pady = (10, 10), fill = 'y')

            self.template_button = ttk.Button(right_frame, text=f"下载添加{self.app}模板")
            self.template_button.pack(padx = (10, 10), pady = (10, 10), fill = 'y')

            self.BacthAdd_button = ttk.Button(right_frame, text = f"批量添加{self.app}")
            self.BacthAdd_button.pack(padx = (10, 10), pady = (10, 10), fill = 'y')

            self.delete_button = ttk.Button(right_frame, text=f"删除{self.app}")
            self.delete_button.pack(padx = (10, 10), pady = (10, 10), fill = 'y')

            self.search_button = ttk.Button(right_frame, text=f"查找{self.app}")
            self.search_button.pack(padx = (10, 10), pady = (10, 10), fill = 'y')
            self.search_entry = ttk.Entry(right_frame)
            self.search_entry.pack(padx = (10, 10), pady = (10, 10), fill = 'y')
        if (init_data):
            self.treeview.insert_manny(init_data)

