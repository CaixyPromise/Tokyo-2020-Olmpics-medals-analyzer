from dataclasses import dataclass, asdict, fields, astuple


@dataclass
class Competition:
    __tablename__ = 'competitions'
    competition_id: str
    time: str
    main_event: str # 比赛大项
    competition_name: str
    venue: str      # 比赛地点
    competition_type : str # 比赛类型
    status: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table(self):
        sql = f"""CREATE TABLE {self.__tablename__} (
    competition_id TEXT PRIMARY KEY,
    time TEXT NOT NULL,
    main_event TEXT NOT NULL,
    competition_name TEXT NOT NULL,
    venue TEXT NOT NULL,
    status TEXT NOT NULL,
    competition_type TEXT NOT NULL,    
);

CREATE INDEX idx_main_event ON {self.__tablename__}(main_event);"""

        return sql
