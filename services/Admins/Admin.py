from db.DatabaseConnection import DatabaseConnection
from services.rank.Service import MedalRankService
from services.races.Service import CompetitionsService


class AdminService(DatabaseConnection):
    def __init__(self):
        super(AdminService, self).__init__()
        self.__medal = MedalRankService()
        self.__race = CompetitionsService()

    def query_medal_rank(self):
        return self.__medal.query_all_rank()

    def query_medal_rank_by_CountryID(self, country_id):
        return self.__medal.query_rank_by_cid(country_id)

    def query_all_race(self):
        return self.__race.query_all_competitions()

    # 新增比赛
    def insert_match(self, competition):
        self.__race.insert_competition(competition)

    # 批量新增比赛
    def insert_matchmany(self, competition):
        self.__race.insert_competition(competition)

    # 修改比赛
    def modify_match(self, competition):
        self.__race.update_competition_by_id(competition)

    # 删除比赛
    def delete_match(self, competition_id):
        self.__race.delete_competition_by_id(competition_id)
