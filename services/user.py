from db.DatabaseConnection import DatabaseConnection
from models.Users import Users
from typing import List, Optional
from response.login import LoginVerifyResponse


class UserService(DatabaseConnection):
    def __init__(self):
        super(DatabaseConnection, self).__init__()

    # def insert_user(self, id, username, password_hash, role, group_id, public_userid):
    def inser_user(self, UserResponse: Users):
        sql = "INSERT INTO users (id, username, password_hash, role, group_id, public_userid) VALUES (?, ?, ?, ?, ?, ?)"
        self.execute(sql, args = (UserResponse.id,
                                  UserResponse.username,
                                  UserResponse.password_hash,
                                  UserResponse.role,
                                  UserResponse.group_id,
                                  UserResponse.public_userid),
                     commit = True)

    def insert_usermany(self, user_list: List[Optional[Users]]):
        sql = "INSERT INTO users (id, username, password_hash, role, group_id, public_userid) VALUES (?, ?, ?, ?, ?, ?)"
        self.execute(sql, args = [v.to_tuple() for v in user_list], commit = True)

    def query_user(self, UserResponse : LoginVerifyResponse):
        sql = "SELECT * FROM users WHERE public_userid=?"
        return self.execute(sql, args = (UserResponse.public_id,), ret = 'one')

    def modify_user(self, UserResponse: Users):
        # def modify_user(self, id, username, password_hash, role, group_id, public_userid):
        sql = "UPDATE users SET username=?, password_hash=?, role=?, group_id=?, public_userid=? WHERE id=?"
        self.execute(sql, args = (UserResponse.username,
                                  UserResponse.password_hash,
                                  UserResponse.role,
                                  UserResponse.group_id,
                                  UserResponse.public_userid,
                                  UserResponse.id),
                     commit = True)
        # self.commit()

    def delete_user(self, UserResponse: Users):
        sql = "DELETE FROM users WHERE id=?"
        self.execute(sql, args = (UserResponse.id), commit = True)
        # self.commit()
