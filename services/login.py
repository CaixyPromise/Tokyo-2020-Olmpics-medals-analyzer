from utils.account import login_user
from db.DatabaseConnection import DatabaseConnection
import sqlite3
from models.Users import Users
from services.user import UserService
from response.login import LoginVerifyResponse, LoginResponse
from response.User import UserConfig


# class UserOperations(DatabaseConnection):
#     def register(self, username, password_hash, role, group_id, public_userid):
#         try:
#             self.execute(
#                 "INSERT INTO users (username, password_hash, role, group_id, public_userid) VALUES (?, ?, ?, ?, ?)",
#                 (username, password_hash, role, group_id, public_userid)
#                 )
#             self.commit()
#             return True
#         except sqlite3.IntegrityError:  # 如果 public_userid 不是唯一的
#             return False
#         finally:
#             self.close()
#
#     def login(self, public_userid):
#         conn = self.connect()
#         c = conn.cursor()
#         c.execute("SELECT * FROM users WHERE public_userid=?", (public_userid,))
#         user = c.fetchone()
#         self.close()
#         if user:
#             return user
#         else:
#             return False
#
#     def delete_password(self, public_userid):
#         conn = self.connect()
#         c = conn.cursor()
#         c.execute("UPDATE users SET password_hash='' WHERE public_userid=?", (public_userid,))
#         conn.commit()
#         self.close()
#
#     def change_password(self, public_userid, new_password_hash):
#         conn = self.connect()
#         c = conn.cursor()
#         c.execute("UPDATE users SET password_hash=? WHERE public_userid=?", (new_password_hash, public_userid))
#         conn.commit()
#         self.close()


class LoginServices:
    __db = UserService()

    def __init__(self):
        # 初始化数据库
        self.__db.connect()

    @classmethod
    def login(cls, response : LoginResponse):
        result : list = cls.__db.query_user(LoginVerifyResponse(response.public_id))
        if (result):
            if (login_user(response.password, result[2])):
                result = list(result)
                config = UserConfig(_id = result[0],
                                    username = result[1],
                                    role = result[3],
                                    group_id = result[4],
                                    public_userid = result[5],
                                    )
                return config
        return False

    # @classmethod
    # def register(cls, public_userid):
    #     # 注册用户
    #     if (cls.__db.register(public_userid)):
    #         return True
    #     return False
