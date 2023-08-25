import tkinter.ttk as ttk
import tkinter as tk
from ui.MainWindow import MainWindow
from ui.LoginWindow import LoginWindow




class App(LoginWindow):
    def __init__(self, parent : tk.Tk):
        super().__init__(parent)
        self.__master = parent
        self.setup_login()


    def __show_psw(self,):
        if self.var.get():
            self.textbox_password.config(show = '')
        else:
            self.textbox_password.config(show = '*')
        self.textbox_password.update_idletasks()

    def enter_index(self):
        self.index_frame = MainWindow(tk.Toplevel(self.__master))
        self.index_frame.pack()

    def setup_login(self):
        self.show_psw.config(command = self.__show_psw)


def main():
    root = tk.Tk()
    root.title("2020东京奥运会奖牌榜管理程序beta v1.0")

    # 设置主题
    root.tk.call("source", "theme/azure.tcl")
    root.tk.call("set_theme", "light")
    # root.iconbitmap('static/image/ico.ico')  # 设置窗口图标
    # icon = tk.PhotoImage(file = 'static/image/ico.png')
    # root.wm_iconphoto(True, icon)
    # 创建应用程序
    app = App(root)
    app.pack(fill = "both", expand = True)

    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))

    root.geometry("%dx%d+%d+%d"%(500,300,x,y))
    root.mainloop()
if __name__ == '__main__':
    main()
