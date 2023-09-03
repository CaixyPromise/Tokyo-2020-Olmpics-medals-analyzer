from db.DatabaseConnection import DatabaseConnection
from models.competition import Competition
from typing import List
from response.competition import CompetitionsResponse


class CompetitionsService(DatabaseConnection):
    __tablename__ = "competitions"

    def __init__(self) -> None:
        super(CompetitionsService, self).__init__()

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
                     commit = True
                     )

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

    def query_competition_by_id(self, competition_id):
        sql = f"SELECT * FROM {self.__tablename__} WHERE competition_id=?"
        result = self.execute(sql, args = (competition_id,), ret = 'one')
        if (result):
            return CompetitionsResponse(*result)
        return None

    def update_competition_by_id(self, competition):
        print(f'competion: {competition}')
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
