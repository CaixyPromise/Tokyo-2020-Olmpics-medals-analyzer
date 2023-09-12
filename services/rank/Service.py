from db.DatabaseConnection import DatabaseConnection
from models.RewardRecord import MedalLog
from response.medal import MedalRaceInfo
from response.rank import MedalRankResponse
from models.medal_Rank import Medal_rank
from typing import List

from response.reward import MedalLogResponse
from utils.upload_file import delete_files, rename_files


class MedalRankService(DatabaseConnection):
    __tablename__ = "medal_rank"

    def __init__(self) -> None:
        super(MedalRankService, self).__init__()

    def __fetch_player_account(self, public_id):
        sql = f"SELECT public_userid FROM users WHERE username = '{public_id}'"
        fecth_result = self.execute(sql, ret = 'one')
        return fecth_result[0]

 
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

    def query_reward(self):
        sql = """
    SELECT 
        medal_log.race_name,
        medal_log.gold_country_code,
        users1.public_userid AS gold_player_public_id,
        medal_log.silver_country_code,
        users2.public_userid AS silver_player_public_id,
        medal_log.bronze_country_code,
        users3.public_userid AS bronze_player_public_id
    FROM 
        medal_log
    LEFT JOIN users AS users1 ON medal_log.gold_player_id = users1.username
    LEFT JOIN users AS users2 ON medal_log.silver_player_id = users2.username
    LEFT JOIN users AS users3 ON medal_log.bronze_player_id = users3.username
"""
        result = self.execute(sql, ret = 'all')
        return [MedalRaceInfo(*row) for row in result]

    def insert_medal(self, response):
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

    def update_medal(self, current_medal_info : MedalLogResponse, new_medal_info: MedalLogResponse):
        # 1. 获取当前的奖牌信息
        race_id = current_medal_info.race_id
        # sql = "SELECT * FROM medal_log WHERE race_id = ?"
        # current_medal_info = self.execute(sql, args = (race_id,), ret = 'one')

        # 2. 对比新旧信息，找出变化的国家
        changed_countries = {}
        for medal_type in ['gold', 'silver', 'bronze']:
            old_code = getattr(current_medal_info, f"{medal_type}_country_code")
            new_code = getattr(new_medal_info, f"{medal_type}_country_code")

            if old_code != new_code:
                changed_countries[medal_type] = (old_code, new_code)
                if (medal_type == 'gold'):
                    old_play_id =  self.__fetch_player_account(current_medal_info.gold_player_id)
                    new_play_id = self.__fetch_player_account(new_medal_info.gold_player_id)
                elif (medal_type == 'silver'):
                    old_play_id = self.__fetch_player_account(current_medal_info.silver_player_id)
                    new_play_id = self.__fetch_player_account(new_medal_info.silver_player_id)
                else:
                    old_play_id = self.__fetch_player_account(current_medal_info.bronze_player_id)
                    new_play_id = self.__fetch_player_account(new_medal_info.bronze_player_id)
                rename_files(current_medal_info.race_id,
                             current_medal_info.race_name,
                             old_player = old_play_id,
                             new_player = new_play_id)

        # 3. 更新 medal_log 表
        sql = """
            UPDATE medal_log SET 
            race_name = ?, gold_country_code = ?, gold_player_id = ?, 
            silver_country_code = ?, silver_player_id = ?,
            bronze_country_code = ?, bronze_player_id = ?
            WHERE race_id = ?
            """
        self.execute(sql, args = (new_medal_info.race_name, new_medal_info.gold_country_code, new_medal_info.gold_player_id,
                                  new_medal_info.silver_country_code, new_medal_info.silver_player_id,
                                  new_medal_info.bronze_country_code, new_medal_info.bronze_player_id,
                                  race_id), commit = True
                     )

        # 4. 更新 medal_rank 表
        for medal_type, (old_code, new_code) in changed_countries.items():
            # 减少旧国家的奖牌数
            if old_code:
                sql = f"UPDATE medal_rank SET {medal_type} = {medal_type} - 1, count = count - 1 WHERE countryid = ?"
                self.execute(sql, args = (old_code,), commit = True)

            # 增加新国家的奖牌数
            if new_code:
                sql = f"UPDATE medal_rank SET {medal_type} = {medal_type} + 1, count = count + 1 WHERE countryid = ?"
                self.execute(sql, args = (new_code,), commit = True)
        # 5. 更新 reward_record 表
        # 删除旧的记录
        sql = "DELETE FROM reward_record WHERE race_id = ?"
        self.execute(sql, args = (race_id,), commit = True)

        # 插入新的记录
        for medal_type in ['gold', 'silver', 'bronze']:
            new_player = getattr(new_medal_info, f"{medal_type}_player_id")
            if new_player:
                sql = "INSERT INTO reward_record (player_id, race_id, race_name) VALUES (?, ?, ?)"
                self.execute(sql, args = (new_player, race_id, new_medal_info.race_name), commit = True)

    def delete_medal_info(self, current_medal_info:MedalLogResponse):
        # 1. 获取当前的奖牌信息
        race_id = current_medal_info.race_id

        # 2. 更新 medal_rank 表
        for medal_type in ['gold', 'silver', 'bronze']:
            old_code = getattr(current_medal_info, f"{medal_type}_country_code")
            # 减少旧国家的奖牌数
            if old_code:
                sql = f"UPDATE medal_rank SET {medal_type} = {medal_type} - 1, count = count - 1 WHERE countryid = ?"
                self.execute(sql, args = (old_code,), commit = True)
                if (medal_type == 'gold'):
                    play_id =  self.__fetch_player_account(current_medal_info.gold_player_id)
                elif (medal_type == 'silver'):
                    play_id = self.__fetch_player_account(current_medal_info.silver_player_id)
                else:
                    play_id = self.__fetch_player_account(current_medal_info.bronze_player_id)
                delete_files(current_medal_info.race_id,
                             current_medal_info.race_name,
                             player = play_id)
        # 3. 删除 medal_log 表中的记录
        sql = "DELETE FROM medal_log WHERE race_id = ?"
        self.execute(sql, args = (race_id,), commit = True)

        # 4. 删除 reward_record 表中的记录
        sql = "DELETE FROM reward_record WHERE race_id = ?"
        self.execute(sql, args = (race_id,), commit = True)

    def query_reward_log(self):
        sql = """
        SELECT 
        race_id, race_name, 
        gold_country_code, gold_player_id,
        silver_country_code, silver_player_id, 
        bronze_country_code, bronze_player_id 
        FROM medal_log;
        """
        return [MedalLogResponse(*v) for v in self.execute(sql, ret = 'all')]

    # 新增奖牌插入日志
    def insert_medal_log(self, reponse:MedalLogResponse):
        sql = """
        INSERT INTO medal_log (
            race_id, race_name, 
            gold_country_code, gold_player_id,
            silver_country_code, silver_player_id, 
            bronze_country_code, bronze_player_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.execute(sql, args = reponse.to_tuple(), commit = True)

    def modify_medal_info(self, medal_node):
        sql = f"UPDATE medal_rank SET rank=?, gold=?, silver=?, bronze=?, count=? WHERE countryid=?"
        self.execute(sql, args = (medal_node.rank,
                                  medal_node.gold,
                                  medal_node.silver,
                                  medal_node.bronze,
                                  medal_node.count,
                                  medal_node.countryid,), commit = True)