from dataclasses import dataclass, astuple, asdict, fields

@dataclass
class Users:
    __tablename__ = 'users'
    id: int
    username: str
    password_hash: str
    role: int
    group_id: str
    public_userid: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table(self):
        sql = f"""CREATE TABLE {self.__tablename__}
(
    id INTEGER,
    username TEXT,
    password_hash TEXT,
    role INTEGER,
    group_id TEXT,
    public_userid TEXT UNIQUE
);"""
        return sql