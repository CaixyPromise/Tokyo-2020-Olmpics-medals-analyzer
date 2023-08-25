

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