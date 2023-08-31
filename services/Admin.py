from db.DatabaseConnection import DatabaseConnection
from models.medal_Rank import Medal_rank
from services.medal_rank import MedalRankService

class AdminService(DatabaseConnection):
    def __init__(self):
        super(AdminService, self).__init__()


    def query_medal_rank(self):
        return MedalRankService().query_all_rank()

    def query_medal_rank_by_CountryID(self, country_id):
        return MedalRankService().query_rank_by_cid(country_id)

    # 新增比赛
    def insert_match(self):
        pass

    # 批量新增比赛
    def insert_matchmany(self):
        pass

    # 修改比赛
    def modify_match(self):
        pass

    # 删除比赛
    def delete_match(self):
        pass

    # 新增比赛项目
    def insert_project(self):
        pass

    # 批量新增比赛项目
    def insert_projectmany(self):
        pass
