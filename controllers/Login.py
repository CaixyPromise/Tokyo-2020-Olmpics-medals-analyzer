from services.login import LoginServices
from response.login import LoginVerifyResponse, LoginResponse
from utils.account import login_user
from response.User import UserConfig


class LoginControllers:
    def __init__(self):
        self.__service = LoginServices()

    def login(self, response : LoginResponse):
        result = self.__service.query_user(LoginVerifyResponse(response.public_id))
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