from dataclasses import dataclass, astuple, asdict, fields, field

@dataclass
class Users:
    __tablename__ = 'users'
    username: str
    password_hash: str
    role: int
    group_id: str
    public_userid: str
    user_contact : str
    id_: int = field(default = -1, init = False)


    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table(self):
        sql = f"""create table {self.__tablename__}(
    id            INTEGER
        primary key autoincrement,
    username      TEXT,
    password_hash TEXT,
    role          INTEGER,
    group_id      TEXT,
    public_userid TEXT
        unique,
    user_contact  TEXT
);"""
        return sql