from dataclasses import dataclass, asdict, fields, astuple, field

@dataclass
class Medal_rank:
    __tablename__ =  'medal_rank'
    rank : int
    countryname : str
    countryid : str
    gold : int
    silver : int
    bronze : int
    count : int

    def to_tuple(self):
        return astuple(self)
    def to_dict(self):
        return asdict(self)
    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table(self):
        sql = f"""create table {self.__tablename__}
(
    rank        INTEGER not null,
    countryname TEXT,
    countryid   TEXT
        primary key
        unique,
    gold        INTEGER,
    silver      INTEGER,
    bronze      INTEGER,
    count       INTEGER
);

create index medal_rank_countryid_index
    on medal_rank (countryid);"""
        return sql

