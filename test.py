

# # 连接到SQLite数据库（如果不存在，则会创建一个新的数据库文件）
# conn = sqlite3.connect("medalsDB")
# cursor = conn.cursor()
#
# # 创建用户表单
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT,
#         password_hash TEXT,
#         role INTEGER,
#         group_id TEXT
#     )
# ''')
#
# # 插入示例管理员用户
# password = "admin"  # 实际中应该使用更安全的方式来管理密码
# add_salt_password = register_user(password)
# cursor.execute('''
#     INSERT INTO users (username, password_hash, role, group_id)
#     VALUES (?, ?, ?, ?)
# ''', (
#     "admin",
#     add_salt_password,
#     0,
#     "Admin"
# ))
#
# # 提交更改并关闭连接
# conn.commit()
# # conn.close()
#
#
#
#
# print("用户数据已成功存入SQLite数据库表单。")
#
# # 查询示例管理员用户的哈希密码
# cursor.execute('''
#     SELECT username, password_hash FROM users WHERE username = ?
# ''', ("admin",))
# user_row = cursor.fetchone()
# if user_row:
#     username, hashed_password = user_row
#     login_password = "admin"  # 实际中应该由用户输入
#     print(login_user(login_password, hashed_password))
# else:
#     print("User not found.")
#
# conn.close()


# import ctypes
#
# class LoadDynamicLib:
#     def __init__(self, lib_path = 'utils/DS/DynamicLibaray.dll') -> None:
#         self.lib = ctypes.cdll.LoadLibrary(lib_path)
#         self.lib.init_arr()
#         self.lib.print_arr()
#
# LoadDynamicLib()

# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# def main():
#     root = tk.Tk()
#     root.title("Treeview with Images")
#
#     # Create a Treeview widget
#     tree = ttk.Treeview(root, columns=("Name", "Age"), show='tree headings')
#     tree.heading("#0", text = "Tree Column")
#     tree.heading("#1", text="Name")
#     tree.heading("#2", text="Age")
#
#     # Add data
#     tree.insert("", tk.END, values=("Alice", 30))
#     tree.insert("", tk.END, values=("Bob", 40))
#
#     image = Image.open('static/image/flags/CAN.png')
#
#     image = image.resize((33, 22))
#     photo = ImageTk.PhotoImage(image)
#     # Create a PhotoImage object
#
#     # Insert a row with an image
#     tree.insert("", tk.END, image=photo, values=("Charlie", 50))
#
#     tree.pack()
#
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()

# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
#
#
# def open_image_file(file):
#     image = Image.open(file)
#     image = image.resize((33, 22))
#     photo = ImageTk.PhotoImage(image)
#     return photo
# def main():
#     root = tk.Tk()
#     root.title("Olympics Medal Table")
#     style = ttk.Style()
#     # Set up the Treeview columns
#     tree = ttk.Treeview(root, columns = ("Country", "Gold", "Silver", "Bronze", "Total"), show = 'tree headings')
#     gold_img = open_image_file(file="static/image/gold_medal.png")
#     silver_img = open_image_file(file="static/image/silver_medal.png")
#     bronze_img = open_image_file(file="static/image/bronze_medal.png")
#     # style.layout("Treeview.Heading", [
#     #     ("Treeview.Heading.image", {"side": "left", "sticky": "", }),
#     #     ("Treeview.Heading.cell", {"sticky": "nswe"}),
#     #     ("Treeview.Heading.text", {"side": "left", "sticky": ""})
#     #     ]
#     #              )
#     tree.heading("#0", text = "排名", anchor = tk.CENTER)
#     tree.heading("#1", text = "国家/地区", anchor = tk.CENTER)
#     tree.heading("#2", text = "金牌", anchor = tk.CENTER, image = gold_img, )
#     tree.heading("#3", text = "银牌", anchor = tk.CENTER, image = silver_img)
#     tree.heading("#4", text = "铜牌", anchor = tk.CENTER, image =  bronze_img)
#     tree.heading("#5", text = "总数", anchor = tk.CENTER)
#
#     tree.column("#0", minwidth = 10, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#1", minwidth = 20, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#2", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#3", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#4", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#     tree.column("#5", minwidth = 5, width = 100, stretch = tk.YES, anchor = 'center')
#
#     # Insert sample data with flag images
#     china_flag = open_image_file(file = "static/image/flags/CHN.png")
#     usa_flag = open_image_file(file = "static/image/flags/USA.png")
#
#     tree.insert("", tk.END, text = "1", image = china_flag, values = ("China", 38, 32, 18, 88))
#     tree.insert("", tk.END, text = "2", image = usa_flag, values = ("USA", 35, 28, 23, 86))
#
#     tree.pack()
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()


import tkinter as tk
import re

def validate_time(char, value_if_allowed):
    # 正则表达式用于匹配 24 小时制时间
    pattern = re.compile(r'^(?:[01]?[0-9]|2[0-3]):[0-5][0-9]$')

    # 判断时间格式是否合法
    if pattern.fullmatch(value_if_allowed) or value_if_allowed == "":
        return True
    else:
        return False

# 初始化 Tkinter 应用
root = tk.Tk()
root.title("Time Entry")

# 配置验证命令
validate_command = root.register(validate_time)
time_entry = tk.Entry(
    root,
    validate="key",
    validatecommand=(validate_command, "%S", "%P")  # %S 是触发操作的字符，%P 是允许操作后的新值
)
time_entry.pack(pady=20)

# 添加一个按钮，用于获取输入的时间
def get_time():
    entered_time = time_entry.get()
    if entered_time:
        print(f"Entered time is: {entered_time}")

tk.Button(root, text="Get Time", command=get_time).pack(pady=10)

root.mainloop()
