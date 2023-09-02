from dataclasses import dataclass, asdict, astuple, fields

@dataclass
class NationalTeam:
    __tablename__ = 'national_teams'
    country_code: str
    country_name: str
    team_size: int
    manager_name: str
    manager_contact: str
    manager_identity: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table_sql(self):
        return f"""create table {self.__tablename__}
(
    country_code     TEXT not null
        primary key
        unique,
    country_name     TEXT not null,
    team_size        INTEGER,
    manager_name     TEXT,
    manager_contact  TEXT,
    manager_identity TEXT
);
"""