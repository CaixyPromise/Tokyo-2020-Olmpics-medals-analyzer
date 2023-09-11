from typing import List

from db.DatabaseConnection import DatabaseConnection
from response.reward import MedalLogResponse
from services.rank.Service import MedalRankService
from services.races.Service import CompetitionsService
from services.team.Service import NationalTeamService
from services.user import  UserService


class AdminService(DatabaseConnection):
    def __init__(self):
        super(AdminService, self).__init__()
        self.__medal = MedalRankService()
        self.__race = CompetitionsService()
        self.__team = NationalTeamService()
        self.__user = UserService()

    def insert_coutryAdmin(self, coutryID, contact):
        self.__user.make_coutryAdmin(coutryID, contact)

    def insert_Adminuser(self, usernode):
        self.__user.inser_user(usernode)

    def insert_mannyAdmin(self, dataList):
        self.__user.insert_mannyAdmin(dataList)

    def modify_admin(self, response):
        self.__user.modify_userinfo(response)
    def query_admin(self):
        return  self.__user.query_admin()

    def delete_admin(self, delete_node):
        return self.__user.delete_user(delete_node)

    def query_medal_rank(self):
        return self.__medal.query_all_rank()

    def query_medal_rank_by_CountryID(self, country_id):
        return self.__medal.query_rank_by_cid(country_id)

    def query_all_race(self):
        return self.__race.query_all_competitions()
    def modify_medal(self, medalNode):
        return self.__medal.modify_medal_info(medalNode)

    # 新增比赛
    def insert_match(self, competition):
        self.__race.insert_competition(competition)

    # 批量新增比赛
    def insert_matchmany(self, competition):
        self.__race.insert_manny_competitions(competition)

    # 修改比赛
    def modify_match(self, competition):
        self.__race.update_competition_by_id(competition)

    # 删除比赛
    def delete_match(self, competition_id):
        self.__race.delete_competition_by_id(competition_id)

    #  新增国家
    def insert_team(self, teamNode):
        self.__team.insert_team(teamNode)

    # 批量新增国家
    def insert_teammany(self, teamList):
        self.__team.insert_many_teams(teamList)

    # 修改国家
    def modify_team(self, teamNode):
        self.__team.update_team_by_code(teamNode)

    # 删除国家
    def delete_team(self, team_id):
        self.__team.delete_team_by_code(team_id)

    # 查找全部国家
    def query_all_team(self):
        return self.__team.query_all_teams()

    # 根据国家ID查找
    def query_team_by_id(self, team_id):
        return self.__team.query_team_by_code(team_id)

    # 根据国家名称查找
    def query_team_by_name(self, team_name):
        return self.__team.query_team_by_name(team_name)

    # 新增奖牌
    def insert_medal(self, reponse):
        return self.__medal.insert_medal(reponse)

    # 查询奖牌插入日志
    def query_reward_log(self) -> List[MedalLogResponse]:
        return self.__medal.query_reward_log()

    # 更新奖牌信息
    def update_medal_info(self, cur_response:MedalLogResponse,
                          old_response:MedalLogResponse):
        return self.__medal.update_medal(cur_response, old_response)

    # 删除奖牌信息
    def delete_medal_info(self, response, ):
        return self.__medal.delete_medal_info(response)