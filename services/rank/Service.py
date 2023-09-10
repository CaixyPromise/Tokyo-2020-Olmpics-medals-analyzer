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

    def update_medal(self, response):
        # 检查 race_id 是否在 competitions 表中
        race_check_sql = "SELECT * FROM competitions WHERE competition_id = ?"
        race_exist = self.execute(race_check_sql, (response.race_id,), ret = 'one')
        if not race_exist:
            print("赛事ID不存在，无法进行后续操作")
            return False

        # 检查三个国家代码是否存在
        country_check_sql = "SELECT COUNT(*) FROM medal_rank WHERE countryid = ?"
        gold_exist = self.execute(country_check_sql, (response.gold_code,), ret = 'one')[0]
        silver_exist = self.execute(country_check_sql, (response.silver_code,), ret = 'one')[0]
        bronze_exist = self.execute(country_check_sql, (response.bronze_code,), ret = 'one')[0]

        if gold_exist == 0 or silver_exist == 0 or bronze_exist == 0:
            print("一个或多个国家代码不存在，无法进行后续操作")
            return False

        # 更新金牌国家信息
        update_gold_sql = "UPDATE medal_rank SET gold = gold + 1, count = count + 1 WHERE countryid = ?"
        self.execute(update_gold_sql, (response.gold_code,), commit = True)

        # 更新银牌国家信息
        update_silver_sql = "UPDATE medal_rank SET silver = silver + 1, count = count + 1 WHERE countryid = ?"
        self.execute(update_silver_sql, (response.silver_code,), commit = True)

        # 更新铜牌国家信息
        update_bronze_sql = "UPDATE medal_rank SET bronze = bronze + 1, count = count + 1 WHERE countryid = ?"
        self.execute(update_bronze_sql, (response.bronze_code,), commit = True)

        # 查询运动员的 public_userid
        player_id_sql = "SELECT username FROM users WHERE public_userid = ?"
        gold_username = self.execute(player_id_sql, (response.gold_player,), ret = 'one')[0]
        silver_username = self.execute(player_id_sql, (response.silver_player,), ret = 'one')[0]
        bronze_username = self.execute(player_id_sql, (response.bronze_player,), ret = 'one')[0]

        # 向 reward_record 表添加信息
        insert_reward_sql = "INSERT INTO reward_record (player_id, race_id, race_name) VALUES (?, ?, ?)"

        self.execute(insert_reward_sql, (gold_username, response.race_id, race_exist[3]), commit = True)
        self.execute(insert_reward_sql, (silver_username, response.race_id, race_exist[3]), commit = True)
        self.execute(insert_reward_sql, (bronze_username, response.race_id, race_exist[3]), commit = True)
        return race_exist[3]
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