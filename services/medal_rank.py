from db.DatabaseConnection import DatabaseConnection
from models.medal_Rank import Medal_rank
from response.rank import MedalRankData

class MedalRankService(DatabaseConnection):
    __tablename__ = "medal_rank"

    def __init__(self) -> None:
        super(MedalRankService, self).__init__()

    def query_all_rank(self):
        sql = f"SELECT * FROM {self.__tablename__}"
        fecth_result = self.execute(sql, ret = 'all')
        
        return [MedalRankData(val[0], val[1],
                              val[2], val[3],
                              val[4], val[5],
                              val[6])
                for val in fecth_result]

    def query_rank_by_cid(self, cid):
        sql = f"SELECT * FROM {self.__tablename__} WHERE countryid=?"
        return self.execute(sql, args = (cid,), ret = 'all')

    # def insert_medal_rank(self, rank, countryname, countryid, gold, silver, bronze, count):
    #     sql = f"INSERT INTO {self.__tablename__} (rank, countryname, countryid, gold, silver, bronze, count) VALUES (?, ?, ?, ?, ?, ?, ?)"
    #     self.execute(sql, args = (rank, countryname, countryid, gold, silver, bronze, count))
    #     self.commit()
    #
    # def modify_medal_info(self, rank, gold, silver, bronze, count, id):
    #     sql = f"UPDATE {self.__tablename__} SET rank=?, gold=?, silver=?, bronze=?, count=? WHERE id=?"
    #     self.execute(sql, args = (rank, gold, silver, bronze, count, id))
    #     self.commit()

    def delete_medal_rank(self, id):
        sql = f"DELETE FROM {self.__tablename__} WHERE id=?"
        self.execute(sql, args = (id,), commit = True)