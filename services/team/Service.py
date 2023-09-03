from db.DatabaseConnection import DatabaseConnection
from models.team import NationalTeam
from response.team import  TeamResponse
from typing import List

class NationalTeamService(DatabaseConnection):
    __tablename__ = "national_teams"

    def __init__(self) -> None:
        super(NationalTeamService, self).__init__()

    def insert_team(self, team: NationalTeam):
        sql = f"""INSERT INTO {self.__tablename__} (country_code, country_name, team_size, 
                  manager_name, manager_contact, manager_identity) VALUES (?, ?, ?, ?, ?, ?)"""
        self.execute(sql, args = (team.country_code,
                                  team.country_name,
                                  team.team_size,
                                  team.manager_name,
                                  team.manager_contact,
                                  team.manager_identity),
                     commit = True
                     )

    def insert_many_teams(self, teams: List[NationalTeam]):
        sql = f"""INSERT INTO {self.__tablename__} (country_code, country_name, team_size, 
                  manager_name, manager_contact, manager_identity) VALUES (?, ?, ?, ?, ?, ?)"""
        data = [team.to_tuple() for team in teams]
        self.execute_manny(sql, data)

    def delete_team_by_code(self, country_code):
        sql = f"DELETE FROM {self.__tablename__} WHERE country_code=?"
        self.execute(sql, args = (country_code,), commit = True)

    def query_all_teams(self):
        sql = f"SELECT * FROM {self.__tablename__}"

        return [NationalTeam(*v) for v in self.execute(sql, ret = 'all')]

    def query_team_by_code(self, country_code):
        sql = f"SELECT * FROM {self.__tablename__} WHERE country_code=?"
        result = self.execute(sql, args = (country_code,), ret = 'one')
        if (result):
            return TeamResponse(*result)
        return None

    def query_team_by_name(self, country_name):
        sql = f"SELECT * FROM {self.__tablename__} WHERE country_name=?"
        result = self.execute(sql, args = (country_name,), ret = 'one')
        if (result):
            return TeamResponse(*result)
        return None

    def update_team_by_code(self, team):
        sql = f"""UPDATE {self.__tablename__} SET country_name=?, team_size=?, 
                  manager_name=?, manager_contact=?, manager_identity=? WHERE country_code=?"""
        return self.execute(sql, args = (team.country_name,
                                         team.team_size,
                                         team.manager_name,
                                         team.manager_contact,
                                         team.manager_identity,
                                         team.country_code,),
                            commit = True)
