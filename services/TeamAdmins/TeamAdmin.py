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