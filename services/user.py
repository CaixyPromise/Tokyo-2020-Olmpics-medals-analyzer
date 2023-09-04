from db.DatabaseConnection import DatabaseConnection
from models.Users import Users
from typing import List, Optional
from response.login import LoginVerifyResponse
from utils.account import register_user
from response.User import UserResponse, UserDeleteResponse, UserAddAdminResponse, UserModifyResponse


class UserService(DatabaseConnection):
    def __init__(self):
        super(UserService, self).__init__()

    def inser_user(self, response: Users):
        sql = "INSERT INTO users ( username, password_hash, role, group_id, public_userid, user_contact) VALUES ( ?, ?, ?, ?, ?, ?)"
        if (isinstance(response.password_hash, str)):
            response.password_hash = register_user(response.password_hash)
        self.execute(sql, args = (response.username,
                                  response.password_hash,
                                  response.role,
                                  response.group_id,
                                  response.public_userid,
                                  response.user_contact),
                     commit = True
                     )
    def insert_mannyAdmin(self, dataList : List[UserAddAdminResponse]):
        sql = "INSERT INTO users ( username,public_userid, user_contact, role, group_id, password_hash ) VALUES ( ?, ?, ?, ?, ?, ?)"
        all_data = []
        for data in dataList:
            data.password_hash = register_user('123456')
            data.role = 0
            data.group_id = 'Admin'
            all_data.append(data.to_tuple())
        self.execute_manny(sql, data = all_data)

    def make_coutryAdmin(self, coutry_id, contact):
        new_user = Users(f"{coutry_id}_admin", register_user("123456"), 1, coutry_id, coutry_id, user_contact = contact)
        self.inser_user(new_user)

    def make_coutryPlayer(self, coutry_id, name, contact):
        new_user = Users(f"{coutry_id}_{name}", "123456", 1, coutry_id, f"{coutry_id}_{name}", user_contact = contact)
        self.inser_user(new_user)

    def insert_usermany(self, user_list: List[Optional[Users]]):
        sql = "INSERT INTO users (id, username, password_hash, role, group_id, public_userid) VALUES (?, ?, ?, ?, ?, ?)"
        self.execute_manny(sql, data = [v.to_tuple() for v in user_list], )

    def Verify_user(self, UserResponse: LoginVerifyResponse):
        sql = "SELECT * FROM users WHERE public_userid=?"
        return self.execute(sql, args = (UserResponse.public_id,), ret = 'one')

    def query_admin(self):
        sql = "SELECT username, public_userid,user_contact FROM users WHERE role=0"
        return [UserResponse(*fecth_data) for fecth_data in
                self.execute(sql, ret = 'all')
                ]

    def modify_user(self, UserResponse: Users):
        sql = "UPDATE users SET username=?, password_hash=?, role=?, group_id=?, public_userid=?, user_contact=?WHERE id=?"
        self.execute(sql, args = (UserResponse.username,
                                  UserResponse.password_hash,
                                  UserResponse.role,
                                  UserResponse.group_id,
                                  UserResponse.public_userid,
                                  UserResponse.id_,
                                  UserResponse.user_contact),
                     commit = True
                     )
        # self.commit()

    def delete_admin(self, Response: UserDeleteResponse):
        sql = "DELETE FROM users WHERE public_userid=?"
        self.execute(sql, args = (Response.public_userid,), commit = True)
    def modify_admin(self, respose : UserModifyResponse):
        sql = "UPDATE users SET username = ?, user_contact = ? WHERE public_userid=?"
        print(f'response: {(respose.username, respose.public_userid, respose.user_contact ,)}')
        self.execute(sql, args = (respose.username, respose.user_contact, respose.public_userid, ), commit = True)

