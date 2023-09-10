from tkinter import Toplevel, ttk
import tkinter as tk
from datetime import datetime
from tkinter.messagebox import showerror
from tkcalendar import DateEntry


class AskUserQuestionDialog(Toplevel):
    def __init__(self, name, part_dict: dict, return_val = None):
        super(AskUserQuestionDialog, self).__init__()
        self.title(name)
        self.resizable(False, False)
        self.answer_dict = {}
        self.result = return_val
        self.part_configs = part_dict

        # for row, v in enumerate(part_dict.items()):
        #     columnName, column_info = v
        #     ttk.Label(self, text = columnName).grid(row = row, column = 0, padx = (10, 10), pady = (10, 10),
        #                                             sticky = tk.NSEW
        #                                             )
        #     if (column_info['type'] == 'time'):
        #         tmp_entry = ttk.Frame(self)
        #         self.__Date = DateEntry(tmp_entry, date_pattern = 'y-mm-dd', selectmode = 'readonly')
        #         self.__Date.grid(row = 0, column = 0, padx = (0, 10), sticky = tk.NSEW)
        #         self.__hour_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 23, width = 5, wrap = True, format = "%02.0f")
        #         self.__minute_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True,
        #                                          format = "%02.0f"
        #                                          )
        #         self.__second_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True,
        #                                          format = "%02.0f"
        #                                          )
        #
        #         self.__hour_spin.grid(row = 0, column = 1, padx = (0, 10), sticky = tk.NSEW)
        #         tk.Label(tmp_entry, text = ":").grid(row = 0, column = 2, padx = (0, 10), sticky = tk.NSEW)
        #         self.__minute_spin.grid(row = 0, column = 3, padx = (0, 10), sticky = tk.NSEW)
        #         tk.Label(tmp_entry, text = ":").grid(row = 0, column = 4, padx = (0, 10), sticky = tk.NSEW)
        #         self.__second_spin.grid(row = 0, column = 5, padx = (0, 10), sticky = tk.NSEW)
        #         tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
        #         self.answer_dict[columnName] = tmp_entry
        #
        #     elif (column_info['type'] == 'combobox'):
        #         tmp_entry = ttk.Combobox(self, width = 10,
        #                                  state = 'readonly',
        #                                  values = column_info['value']
        #                                  )
        #         tmp_entry.current(0)
        #         tmp_entry.grid(row = row, column = 1,
        #                        padx = (10, 10), pady = (10, 10),
        #                        sticky = tk.NSEW)
        #         self.answer_dict[columnName] = tmp_entry
        #     else:
        #         tmp_entry = ttk.Entry(self)
        #         tmp_entry.grid(row = row, column = 1,
        #                        padx = (10, 10), pady = (10, 10),
        #                        sticky = tk.NSEW)
        #     self.answer_dict[columnName] = tmp_entry
        for row, (columnName, column_info) in enumerate(self.part_configs.items()):
            ttk.Label(self, text = columnName).grid(row = row, column = 0, padx = (10, 10), pady = (10, 10),
                                                    sticky = tk.NSEW
                                                    )
            col_start = 1  # 初始列

            if column_info['type'] == 'multi-part':
                for col, col_info in enumerate(column_info['cols']):
                    widget, insert = self.__create_widget(col_info)
                    widget.grid(row = row, column = col_start, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
                    col_start += 1
                    if (insert):
                        self.answer_dict[f'{columnName}_{col_start}'] = widget
            else:
                widget, _ = self.__create_widget(column_info)
                widget.grid(row = row, column = col_start, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
                self.answer_dict[columnName] = widget

        self.submit_button = ttk.Button(self, text = "提交", command = self.submit)
        self.submit_button.grid(row = len(self.part_configs) + 1, column = 0,
                                columnspan = 2, sticky = tk.NSEW,
                                padx = (10, 10), pady = (10, 10)
                                )
    def __create_time_widget(self):
        tmp_entry = ttk.Frame(self)
        self.__Date = DateEntry(tmp_entry, date_pattern = 'y-mm-dd', selectmode = 'readonly')
        self.__Date.grid(row = 0, column = 0, padx = (0, 10), sticky = tk.NSEW)
        self.__hour_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 23, width = 5, wrap = True, format = "%02.0f")
        self.__minute_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True,
                                         format = "%02.0f"
                                         )
        self.__second_spin = ttk.Spinbox(tmp_entry, from_ = 0, to = 59, width = 5, wrap = True,
                                         format = "%02.0f"
                                         )

        self.__hour_spin.grid(row = 0, column = 1, padx = (0, 10), sticky = tk.NSEW)
        tk.Label(tmp_entry, text = ":").grid(row = 0, column = 2, padx = (0, 10), sticky = tk.NSEW)
        self.__minute_spin.grid(row = 0, column = 3, padx = (0, 10), sticky = tk.NSEW)
        tk.Label(tmp_entry, text = ":").grid(row = 0, column = 4, padx = (0, 10), sticky = tk.NSEW)
        self.__second_spin.grid(row = 0, column = 5, padx = (0, 10), sticky = tk.NSEW)
        # tmp_entry.grid(row = row, column = 1, padx = (10, 10), pady = (10, 10), sticky = tk.NSEW)
        return tmp_entry

    def __create_widget(self, info):
        if info['type'] == 'text':
            return ttk.Entry(self), True
        elif info['type'] == 'combobox':
            combobox = ttk.Combobox(self, width = 10, state = 'readonly', values = info['value'])
            combobox.current(0)
            return combobox, True
        elif info['type'] == 'time':
            return self.__create_time_widget(), True
        elif info['type'] == 'label':
            return ttk.Label(self, text = info.get('text', '标签')), False
        elif info['type'] == 'button':
            return ttk.Button(self, text = info.get('text', '按钮'),
                              command =  info.get('command', lambda: None)), False


        else:
            return None


    def __get_time(self):
        date = self.__Date.get_date()
        selected_time = f"{self.__hour_spin.get()}:{self.__minute_spin.get()}:{self.__second_spin.get()}"

        return self.checkTime(f"{date} {selected_time}")

    def checkTime(self, date_str):
        """
        获取传入time，校验合法性
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_str
        except ValueError:
            showerror(title = '错误', message = '请输入正确的日期时间')
            return False

    def submit(self):
        return_answer = []
        Append = return_answer.append
        print(self.answer_dict)
        for columnName, column_data in self.part_configs.items():
            if column_data['type'] == 'time':
                val = self.__get_time()
                if (val):
                    Append(val)
                else:
                    return
            elif column_data['type'] == 'multi-part':
                multi_answers = []
                for col in range(len(column_data['cols'])):
                    widget_key = f"{columnName}_{col + 1}"
                    if widget_key in self.answer_dict:
                        widget = self.answer_dict[widget_key]
                        if hasattr(widget, 'get'):
                            multi_answers.append(widget.get())
                Append(multi_answers)
            else:
                if hasattr(self.answer_dict[columnName], 'get'):
                    Append(self.answer_dict[columnName].get())

        if (isinstance(self.result, tk.Variable)):
            self.result.set(return_answer)
        else:
            self.result = return_answer
        self.destroy()
