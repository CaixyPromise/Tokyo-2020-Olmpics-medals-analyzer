from tkinter import Toplevel, ttk
import tkinter as tk

class AskUserQuesionDialog(Toplevel):
    def __init__(self, name, return_val : tk.Variable, columns):
        super(AskUserQuesionDialog, self).__init__()
        self.title(name)
        self.resizable(False, False)
        self.answer_dict = {}
        self.return_val = return_val
        self.columns = columns

        for row, column in enumerate(self.columns):
            ttk.Label(self, text=column).grid(row=row, column = 0, padx = (10, 10), pady = (10, 10))
            tmp_entry = ttk.Entry(self)
            tmp_entry.grid(row=row, column=1, padx = (10, 10), pady = (10, 10))

            self.answer_dict[column] = tmp_entry
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=len(self.columns)+1, column=0, columnspan=2, padx = (10, 10), pady = (10, 10))

    def submit(self):
        self.return_val.set(self.answer_dict)
        self.destroy()