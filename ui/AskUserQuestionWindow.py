from tkinter import Toplevel, ttk
import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror

class AskUserQuestionDialog(Toplevel):
    def __init__(self, name,  columns : dict, return_val = None ):
        super(AskUserQuestionDialog, self).__init__()
        self.title(name)
        self.resizable(False, False)
        self.answer_dict = {}
        self.result =  return_val
        self.columns = columns

        for row, v in enumerate(columns.items()):
            columnName, column_info = v
            ttk.Label(self, text=columnName).grid(row=row, column = 0, padx = (10, 10), pady = (10, 10))
            if (column_info['type'] == 'time'):
                tmp_entry = ttk.Frame(self)
                tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10))
                # 年
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 0, padx = (10, 1))
                ttk.Label(tmp_entry, text='-').grid(row = 0, column = 1, padx = (10, 1))
                # 月
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 2, padx = (10, 1))
                ttk.Label(tmp_entry, text = '-').grid(row = 0, column = 3, padx = (10, 1))
                # 日
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 4, padx = (10, 1))
                ttk.Label(tmp_entry, text = ' ').grid(row = 0, column = 5, padx = (10, 1))
                # 时
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 6, padx = (10, 1))
                ttk.Label(tmp_entry, text = ':').grid(row = 0, column = 7, padx = (10, 1))
                # 分
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 8, padx = (10, 1))
                ttk.Label(tmp_entry, text = ':').grid(row = 0, column = 9, padx = (10, 1))
                # 秒
                ttk.Entry(tmp_entry, width = 10).grid(row = 0, column = 10, padx = (10, 1))
                ttk.Label(tmp_entry, text = ':').grid(row = 0, column = 11, padx = (10, 1))
            elif  (column_info['type'] == 'combobox'):
                tmp_entry = ttk.Combobox(self, width = 10,
                                         state = 'readonly',
                                         values = column_info['value'])
                tmp_entry.current(0)
                tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10))
                self.answer_dict[columnName] = tmp_entry
            else:
                tmp_entry = ttk.Entry(self)
                tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10))
            self.answer_dict[columnName] = tmp_entry


        self.submit_button = ttk.Button(self, text="提交", command=self.submit)
        self.submit_button.grid(row=len(self.columns)+1, column=0, columnspan=2, padx = (10, 10), pady = (10, 10))

    def get_frame_data(self, frame):
        """
        获取传入frame里的所有的值
        """
        values = []
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                values.append(child.get())
        year, month, day, hour, minute, second = values
        try:
            return datetime(int(year), int(month), int(day),
                            int(hour), int(minute), int(second)).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            showerror(title = '错误', message = '请输入正确的日期时间')
            return False


    def submit(self):
        return_answer = []
        Append = return_answer.append
        for columnName, columnType in self.columns:
            if columnType == 'date':
                val = self.get_frame_data(self.answer_dict[columnName])
                if (val):
                    Append(val)
                else: return
            else:
                Append(self.answer_dict[columnName].get())

        if (isinstance(self.result, tk.Variable)):
            self.result.set(return_answer)
        else:
            self.result = return_answer
        self.destroy()