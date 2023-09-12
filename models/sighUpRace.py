from dataclasses import dataclass, field, asdict, astuple

@dataclass
class SignUpRace:
    __tablename__ = 'signUp_race'
    id_: int
    race_id: str
    player_id: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def create_table_sql(self):
        return f"""CREATE TABLE {self.__tablename__} (
            id_ INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            race_id TEXT NOT NULL,
            player_id TEXT NOT NULL
        );"""

    @classmethod
    def create_index_sql(cls):
        return f"""CREATE INDEX signUp_race_race_id_index ON {cls.__tablename__} (race_id);"""