import tkinter.ttk as ttk
import tkinter as tk


class LoginWindow(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)

        self.canvas_frame = ttk.Frame(self)

        canvas = tk.Canvas(self, height = 200, width = 500)
        self.image_file = tk.PhotoImage(file = "static/image/welcome.png")
        canvas.create_image(0, 0, anchor = "nw", image = self.image_file)
        canvas.pack(side = "top")

        textbox_uesrname = ttk.Entry(self, )
        # 密码输入框
        self.textbox_password = ttk.Entry(self, show = "*")
        textbox_uesrname.place(x = 160, y = 150)
        self.textbox_password.place(x = 160, y = 190)

        self.var = tk.IntVar(value = 0)
        self.show_psw = ttk.Checkbutton(self, text = '显示密码',
                                        offvalue = 0, onvalue = 1, variable = self.var)
        self.show_psw.place( x = 330, y = 190)


        tk.Label(self, text = "账号：").place(x = 50, y = 150)
        tk.Label(self, text = "密码：").place(x = 50, y = 190)
        self.login_Button = tk.ttk.Button(self, text = "登录", width = 20)
        self.login_Button.place(x = 160, y = 260)