from db.DatabaseConnection import DatabaseConnection
from models.competition import Competition
from response.competition import CompetitionsData  # 假设你有一个响应体用于 Competitions


class CompetitionsService(DatabaseConnection):
    __tablename__ = "competitions"

    def __init__(self) -> None:
        super(CompetitionsService, self).__init__()

    def insert_competition(self, competition : Competition):
        sql = f"""INSERT INTO {self.__tablename__} (competition_id, time, main_event, 
                  competition_name, competition_type, venue, status) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self.execute(sql, args=(competition.competition_id,
                                competition.time,
                                competition.main_event,
                                competition.competition_name,
                                competition.competition_type,
                                competition.venue,
                                competition.status),
                     commit = True)


    def insert_manny_competitions(self, competitions):
        sql = f"""INSERT INTO {self.__tablename__} (competition_id, time, event, 
                  competition_name, venue, competition_status) VALUES (?, ?, ?, ?, ?, ?)"""
        self.execute_manny(sql, competitions)

    def query_competition_by_id(self, competition_id):
        sql = f"SELECT * FROM {self.__tablename__} WHERE competition_id=?"

    def delete_competition_by_id(self, competition_id):
        sql = f"DELETE FROM {self.__tablename__} WHERE competition_id=?"

        self.execute(sql, args=(competition_id,), commit = True)

    def query_all_competitions(self):
        sql = f"SELECT * FROM {self.__tablename__}"
        fetch_result = [Competition(competition_id = v[0],
                                    time = v[1],
                                    main_event = v[2],
                                    competition_name = v[3],
                                    venue = v[4],
                                    status = v[5],
                                    competition_type = v[6]) for v in self.execute(sql, ret='all')]
        print(fetch_result)
        return fetch_result

    def query_competition_by_id(self, competition_id):
        sql = f"SELECT * FROM {self.__tablename__} WHERE competition_id=?"
        return self.execute(sql, args=(competition_id,), ret='one')

    def update_competition_by_id(self, competition):
        sql = f"""UPDATE {self.__tablename__} SET time=?, event=?, 
                  competition_name=?, venue=?, competition_status=? WHERE competition_id=?"""
        self.execute(sql, args=(competition.time, competition.event,
                                competition.competition_name, competition.venue,
                                competition.competition_status, competition.competition_id))
