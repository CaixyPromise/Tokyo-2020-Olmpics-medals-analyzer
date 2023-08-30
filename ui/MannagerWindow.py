import tkinter.ttk as ttk
import tkinter as tk
from ui.utils.TreeviewUtils import TreeViewUtils
from utils.MediaViewer.MediaViewer import  MediaViewer
from tkinter import font
from utils.make_image import make_image

class MannageDialogWindow(ttk.Frame):
    def __init__(self, parent, columns, function, **kwargs):
        super(MannageDialogWindow, self).__init__(parent, **kwargs)
        self.parent = parent
        self.columns = columns.value
        self.function = function.value
        self.setup_ui()

    def setup_ui(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y", expand=True)
        self.treeview = TreeViewUtils(left_frame, columns = self.columns,
                                      show = 'headings')
        right_frame = ttk.Frame(self)
        right_frame.pack(side="right", fill="y", expand=True)
        self.add_button = ttk.Button(right_frame, text=f"添加{self.function}")
        self.add_button.pack(padx = (10, 10), pady = (10, 10))

        self.BacthAdd_button = ttk.Button(right_frame, text = f"批量添加{self.function}")
        self.BacthAdd_button.pack(padx = (10, 10), pady = (10, 10))

        self.edit_button = ttk.Button(right_frame, text=f"修改{self.function}")
        self.edit_button.pack(padx = (10, 10), pady = (10, 10))

        self.delete_button = ttk.Button(right_frame, text=f"删除{self.function}")
        self.delete_button.pack(padx = (10, 10), pady = (10, 10))
        
        self.search_button = ttk.Button(right_frame, text=f"查找{self.function}")
        self.search_button.pack(padx = (10, 10), pady = (10, 10))
        self.search_entry = ttk.Entry(right_frame)
        self.search_entry.pack(padx = (10, 10), pady = (10, 10))

