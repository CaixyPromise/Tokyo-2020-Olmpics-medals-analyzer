from tkinter import Toplevel, ttk
import tkinter as tk

class AskUserQuestionDialog(Toplevel):
    def __init__(self, name,  columns, return_val : tk.Variable = None ):
        super(AskUserQuestionDialog, self).__init__()
        self.title(name)
        self.resizable(False, False)
        self.answer_dict = {}
        self.result =  return_val
        self.columns = columns

        for row, column in enumerate(self.columns):
            ttk.Label(self, text=column).grid(row=row, column = 0, padx = (10, 10), pady = (10, 10))
            tmp_entry = ttk.Entry(self)
            tmp_entry.grid(row=row, column=1, padx = (10, 10), pady = (10, 10))

            self.answer_dict[column] = tmp_entry

        self.submit_button = ttk.Button(self, text="提交", command=self.submit)
        self.submit_button.grid(row=len(self.columns)+1, column=0, columnspan=2, padx = (10, 10), pady = (10, 10))

    def submit(self):
        return_answer = [v.get() for v in self.answer_dict.values()]
        if (isinstance(self.result, tk.Variable)):
            self.result.set(return_answer)
        else:
            self.result = return_answer
        self.destroy()