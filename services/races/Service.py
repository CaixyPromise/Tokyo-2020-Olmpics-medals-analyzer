from db.DatabaseConnection import DatabaseConnection
from models.RewardRecord import RewardRecord
from models.competition import Competition
from typing import List
from response.competition import CompetitionsResponse
from response.reward import RewardRecordResponse, MedalLogResponse


class CompetitionsService(DatabaseConnection):
    __tablename__ = "competitions"

    def __init__(self) -> None:
        super(CompetitionsService, self).__init__()

    def sigh_up_race(self, race_node):
        sql = """INSERT OR IGNORE INTO signUp_race (race_id, player_id) VALUES (?, ?)"""
        cur = self.execute(sql, args = (race_node.race_id, race_node.player_id), commit = True)

        if cur.rowcount == 0:
            raise Exception("数据已存在，无法插入")
        else:
            race_sql = """SELECT * FROM competitions  WHERE  competition_id = ?"""
            cur = self.execute(race_sql, args = (race_node.race_id,), ret = 'one')
            return cur

    def delete_race_sighup(self, race_node):
        sql = """DELETE FROM signUp_race WHERE race_id = ? AND player_id = ?"""
        self.execute(sql, args = (race_node.race_id, race_node.player_id), commit = True)

    def query_race_by_playID(self, play_id):
        sql = """SELECT c.*
FROM signUp_race s
JOIN competitions c ON s.race_id = c.competition_id
WHERE s.player_id = ?"""
        return [Competition(*v) for v in self.execute(sql, args = (play_id,), ret = 'all')]

    def query_reward_by_playID(self, play_id):
        sql = """SELECT   race_id, race_name FROM reward_record WHERE player_id = ?"""
        return [RewardRecordResponse(*v) for v in self.execute(sql, args = (play_id,), ret = 'all')]

    def insert_competition(self, competition: Competition):
        sql = f"""INSERT INTO {self.__tablename__} (competition_id, time, main_event, 
                  competition_name, competition_type, venue, status) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.execute(sql, args = (competition.competition_id,
                                  competition.time,
                                  competition.main_event,
                                  competition.competition_name,
                                  competition.competition_type,
                                  competition.venue,
                                  competition.status),
                     commit = True)

    def insert_manny_competitions(self, competitions : List[Competition]):
        sql = f"""INSERT INTO {self.__tablename__} (competition_id, time, main_event, 
                  competition_name, competition_type, venue, status) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.execute_manny(sql, [competition.to_tuple() for competition in competitions])

    def delete_competition_by_id(self, competition_id):
        sql = f"DELETE FROM {self.__tablename__} WHERE competition_id=?"

        self.execute(sql, args = (competition_id,), commit = True)

    def query_all_competitions(self):
        sql = f"SELECT * FROM {self.__tablename__}"
        fetch_result = [Competition(*v) for v in self.execute(sql, ret = 'all')]
        return fetch_result

    def query_all_competitions_with_status(self, status):
        sql = f"SELECT * FROM competitions WHERE status=?"
        fetch_result = [Competition(*v) for v in self.execute(sql, args = (status,), ret = 'all')]
        return fetch_result


    def query_competition_by_id(self, competition_id):
        sql = f"SELECT * FROM {self.__tablename__} WHERE competition_id=?"
        result = self.execute(sql, args = (competition_id,), ret = 'one')
        if (result):
            return CompetitionsResponse(*result)
        return None

    def update_competition_by_id(self, competition):
        sql = f"""UPDATE {self.__tablename__} SET time=?, main_event=?, 
                  competition_name=?, competition_type=?, venue=?,  status=? WHERE competition_id=?"""
        return self.execute(sql, args = (competition.time,
                                         competition.main_event,
                                         competition.competition_name,
                                         competition.competition_type,
                                         competition.venue,
                                         competition.status,
                                         competition.competition_id,),
                            commit = True)
