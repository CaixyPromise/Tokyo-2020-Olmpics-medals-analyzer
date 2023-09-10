from dataclasses import dataclass, field, asdict, astuple

@dataclass
class RewardRecord:
    __tablename__ = 'reward_record'
    id_: int
    player_id: int
    race_id: str
    race_name: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def create_table_sql(self):
        return f"""CREATE TABLE {self.__tablename__} (
                    id_ INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    player_id INTEGER NOT NULL,
                    race_id TEXT NOT NULL,
                    race_name TEXT NOT NULL
                  );
                  CREATE INDEX reward_recode_player_id_index ON {self.__tablename__} (player_id);
               """