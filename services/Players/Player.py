from db.DatabaseConnection import DatabaseConnection
from services.rank.Service import MedalRankService
from services.races.Service import CompetitionsService
from services.team.Service import NationalTeamService
from services.user import  UserService


class PlayerService(DatabaseConnection):
    def __init__(self):
        super(PlayerService, self).__init__()
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

    def query_race_with_status(self, status = '未开始'):
        return self.__race.query_all_competitions_with_status(status)

    def insert_race_sighup(self, race_node):
        return self.__race.sigh_up_race(race_node)

    def delete_race_sighup(self, race_node):
        return self.__race.delete_race_sighup(race_node)

    def query_race_by_playID(self, play_id):
        return self.__race.query_race_by_playID(play_id)

    def query_reward_by_playID(self, play_id):
        return self.__race.query_reward_by_playID(play_id)