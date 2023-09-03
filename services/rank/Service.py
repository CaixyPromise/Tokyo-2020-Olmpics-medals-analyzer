from db.DatabaseConnection import DatabaseConnection
from response.rank import MedalRankResponse
from models.medal_Rank import Medal_rank
from typing import List

class MedalRankService(DatabaseConnection):
    __tablename__ = "medal_rank"

    def __init__(self) -> None:
        super(MedalRankService, self).__init__()

    def query_all_rank(self):
        sql = f"SELECT * FROM {self.__tablename__}"
        fecth_result = self.execute(sql, ret = 'all')

        return [MedalRankResponse(val[0], val[1],
                                  val[2], val[3],
                                  val[4], val[5],
                                  val[6])
                for val in fecth_result]

    def query_rank_by_cid(self, cid):
        sql = f"SELECT * FROM {self.__tablename__} WHERE countryid=?"
        return self.execute(sql, args = (cid,), ret = 'all')

    def insert_medal_rank(self, medal_node : Medal_rank):
        sql = f"INSERT INTO medal_rank (rank, countryname, countryid, gold, silver, bronze, count) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.execute(sql, args = (medal_node.rank,
                                  medal_node.countryname,
                                  medal_node.countryid,
                                  medal_node.gold,
                                  medal_node.silver,
                                  medal_node.bronze,
                                  medal_node.count),
                      commit = True)
    def insert_medalManny(self, medal_nodes : List[Medal_rank]):
        [self.insert_medal_rank(medal_node) for medal_node in medal_nodes]

    def modify_medal_info(self, medal_node):
        sql = f"UPDATE medal_rank SET rank=?, gold=?, silver=?, bronze=?, count=? WHERE countryid=?"
        self.execute(sql, args = (medal_node.rank,
                                  medal_node.gold,
                                  medal_node.silver,
                                  medal_node.bronze,
                                  medal_node.count,
                                  medal_node.countryid,), commit = True)


    def delete_medal_rank(self, id):
        sql = f"DELETE FROM {self.__tablename__} WHERE id=?"
        self.execute(sql, args = (id,), commit = True)