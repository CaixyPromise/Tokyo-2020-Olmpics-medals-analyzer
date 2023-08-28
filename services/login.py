from utils.account import login_user
from db.DatabaseConnection import DatabaseConnection
import sqlite3

class UserOperations(DatabaseConnection):
    def register(self, username, password_hash, role, group_id, public_userid):
        conn = self.connect()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (username, password_hash, role, group_id, public_userid) VALUES (?, ?, ?, ?, ?)",
                (username, password_hash, role, group_id, public_userid)
                )
            conn.commit()
            return True
        except sqlite3.IntegrityError:  # 如果 public_userid 不是唯一的
            return False
        finally:
            self.close()

    def login(self, public_userid):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE public_userid=?", (public_userid,))
        user = c.fetchone()
        self.close()
        if user:
            return user
        else:
            return False

    def delete_password(self, public_userid):
        conn = self.connect()
        c = conn.cursor()
        c.execute("UPDATE users SET password_hash='' WHERE public_userid=?", (public_userid,))
        conn.commit()
        self.close()

    def change_password(self, public_userid, new_password_hash):
        conn = self.connect()
        c = conn.cursor()
        c.execute("UPDATE users SET password_hash=? WHERE public_userid=?", (new_password_hash, public_userid))
        conn.commit()
        self.close()


class LoginServices:
    __db = UserOperations()

    def __init__(self):
        # 初始化数据库
        self.__db.connect()

    @classmethod
    def login(cls, public_userid, password):
        result : list = cls.__db.login(public_userid)
        if (result):
            if (login_user(password, result[2])):
                result = list(result)
                del result[2]
                return result
        return False

    @staticmethod
    def register(self, public_userid):
        # 注册用户
        if (self.__db.register(public_userid)):
            return True
        return False

    @staticmethod
    def change_password(self, public_userid, new_password):
        # 修改密码
        if (self.__db.change_password(public_userid, new_password)):
            return True
        return False

    @staticmethod
    def delete_password(self, public_userid):
        # 删除密码
        if (self.__db.delete_password(public_userid)):
            return True
        return False