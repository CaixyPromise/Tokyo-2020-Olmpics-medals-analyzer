from db.DatabaseConnection import DatabaseConnection
from services.rank.Service import MedalRankService
from services.races.Service import CompetitionsService
from services.team.Service import NationalTeamService
from services.user import  UserService


class TeamAdminService(DatabaseConnection):
    def __init__(self):
        super(TeamAdminService, self).__init__()
        self.__medal = MedalRankService()
        self.__race = CompetitionsService()
        self.__team = NationalTeamService()
        self.__user = UserService()

    def query_medal_rank(self):
        return self.__medal.query_all_rank()

    def query_medal_rank_by_CountryID(self, country_id):
        return self.__medal.query_rank_by_cid(country_id)

    def query_all_race(self):
        return self.__race.query_all_competitions()

    def query_user_by_id(self, coutry_id):
        return self.__user.query_user_by_id(coutry_id)

    def query_race_team(self):
        return self.__race.query_race_team()

    def insert_player(self, response):
        return self.__user.inser_user(response)

    def insert_manny_player(self, responseList):
        return self.__user.insert_usermany(responseList)

    def delete_player(self, delete_node):
        return self.__user.delete_user(delete_node)

    def modify_player(self, modify_node):
        return self.__user.modify_userinfo(modify_node)