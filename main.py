import tkinter as tk
from services.login import LoginServices
from ui.AdminWindow import AdminWindow
from ui.LoginWindow import LoginWindow
from tkinter.messagebox import showerror
from response.login import LoginResponse
from services.medal_rank import MedalRankService

class App(LoginWindow):
    __screen_width : int
    __screen_height : int

    def __init__(self, parent : tk.Tk, width, height):
        super().__init__(parent)
        self.__screen_width = width
        self.__screen_height = height
        self.__master = parent
        self.setup_login()
        self.__login_services = LoginServices()
        self.textbox_uesrname.focus()
        self.textbox_uesrname.insert(0, "admin")
        self.textbox_password.insert(0, "admin")

    def login(self, event = None):
        username = self.textbox_uesrname.get()
        password = self.textbox_password.get()

        result =  self.__login_services.login(LoginResponse(public_id = username, password = password))
        if result: # 密码正确
            self.enter_index(result)
        else:   # 密码错误
            showerror(title = '错误', message = '用户名或密码错误')
            # 清空密码框
            self.textbox_password.delete(0, 'end')
            self.textbox_password.focus() #  光标移到密码框
            self.textbox_password.update_idletasks() # 更新状态

    def __show_psw(self,):
        if self.var.get():
            self.textbox_password.config(show = '')
        else:
            self.textbox_password.config(show = '*')
        self.textbox_password.update_idletasks()

    def quit_system(self):
        self.destroy()
        exit(0)

    def enter_index(self, UserInfo):
        self.__user_ui = tk.Toplevel(self.__master)
        self.index_frame = AdminWindow(self.__user_ui)
        self.__user_ui.focus()

        self.index_frame.medal_tree.insert()
        self.index_frame.pack()
        self.__user_ui.protocol("WM_DELETE_WINDOW",
                             lambda : [self.__user_ui.destroy(), self.quit_system()])
        # 隐藏self窗口
        self.__master.withdraw()
        self.__master.update_idletasks()
        # 进入主循环
        self.index_frame.mainloop()

    def setup_login(self):
        self.show_psw.config(command = self.__show_psw)
        self.login_Button.config(command =  self.login)
        self.textbox_password.bind('<Return>', self.login)


def main():
    root = tk.Tk()
    root.title("2020东京奥运会奖牌榜管理程序beta v1.0")

    # 设置主题
    root.tk.call("source", "theme/azure.tcl")
    root.tk.call("set_theme", "light")
    # root.iconbitmap('static/image/ico.ico')  # 设置窗口图标
    # icon = tk.PhotoImage(file = 'static/image/ico.png')
    # root.wm_iconphoto(True, icon)

   # 获取屏幕尺寸，并以此为依据设置窗体居中
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    # 创建应用程序
    app = App(root, width, height)
    app.pack(fill = "both", expand = True)
    root.geometry("%dx%d+%d+%d" % (500, 300, (width - 500) / 2,
                                   (height - 300) / 2))
   #  root.geometry()
    root.mainloop()

if __name__ == '__main__':
    main()
