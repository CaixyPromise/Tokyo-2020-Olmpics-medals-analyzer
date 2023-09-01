from tkinter import Toplevel, ttk
import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror
from tkcalendar import DateEntry

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
            ttk.Label(self, text=columnName).grid(row=row, column = 0, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
            if (column_info['type'] == 'time'):
                tmp_entry = ttk.Frame(self)
                self.__Date = DateEntry(tmp_entry, date_pattern='y-mm-dd', selectmode = 'readonly')
                self.__Date.grid(row=0, column=0, padx = (0, 10), sticky = tk.NSEW)
                self.__hour_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 23, width = 5, wrap = True, format = "%02.0f")
                self.__minute_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True, format = "%02.0f")
                self.__second_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True, format = "%02.0f")

                self.__hour_spin.grid(row=0, column=1, padx = (0, 10), sticky = tk.NSEW)
                tk.Label(tmp_entry, text = ":").grid(row=0, column=2, padx = (0, 10), sticky = tk.NSEW)
                self.__minute_spin.grid(row=0, column=3, padx = (0, 10), sticky = tk.NSEW)
                tk.Label(tmp_entry, text = ":").grid(row=0, column=4, padx = (0, 10), sticky = tk.NSEW)
                self.__second_spin.grid(row=0, column=5, padx = (0, 10), sticky = tk.NSEW)
                tmp_entry.grid(row=row, column = 1, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
                self.answer_dict[columnName] = tmp_entry
            elif  (column_info['type'] == 'combobox'):
                tmp_entry = ttk.Combobox(self, width = 10,
                                         state = 'readonly',
                                         values = column_info['value'])
                tmp_entry.current(0)
                tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
                self.answer_dict[columnName] = tmp_entry
            else:
                tmp_entry = ttk.Entry(self)
                tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
            self.answer_dict[columnName] = tmp_entry


        self.submit_button = ttk.Button(self, text="提交", command=self.submit)
        self.submit_button.grid(row=len(self.columns)+1, column=0, columnspan=2, padx = (10, 10), pady = (10, 10))

    def __get_time(self):
        date = self.__Date.get_date()
        selected_time = f"{self.__hour_spin.get()}:{self.__minute_spin.get()}:{self.__second_spin.get()}"
        return f"{date} {selected_time}"

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
        for columnName, column_data in self.columns.items():
            if column_data['type'] == 'time':
                val = self.__get_time()
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