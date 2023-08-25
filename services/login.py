from utils.accountTools import login_user
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

    def login(self, username, password_hash):
        conn = self.connect()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, password_hash))
        user = c.fetchone()
        self.close()
        if user:
            return True
        else:
            return False

    def delete_password(self, username):
        conn = self.connect()
        c = conn.cursor()
        c.execute("UPDATE users SET password_hash='' WHERE username=?", (username,))
        conn.commit()
        self.close()

    def change_password(self, username, new_password_hash):
        conn = self.connect()
        c = conn.cursor()
        c.execute("UPDATE users SET password_hash=? WHERE username=?", (new_password_hash, username))
        conn.commit()
        self.close()


class LoginServices:
    @staticmethod
    def login(user_id, username, password):
        login_user(password)

    @staticmethod
    def register(self, username):
        pass