from dataclasses import dataclass, asdict, astuple, fields

@dataclass
class Country_Awards:
    __tablename__ = 'country_awards'
    id: int
    playid: str
    itemcodename: str
    subitemname: str
    subitemcode: str
    medaltype: str
    itemcode: str
    startdatecn: str
    countryname: str
    playname: str
    medal: int
    totalurl: str
    countryid: str

    def to_tuple(self):
        return astuple(self)
    def to_dict(self):
        return asdict(self)
    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

    def create_table(self):
        sql = f"""CREATE TABLE {self.__tablename__}
(
    id INTEGER PRIMARY KEY,
    playid TEXT,
    itemcodename TEXT,
    subitemname TEXT,
    subitemcode TEXT,
    medaltype TEXT,
    itemcode TEXT,
    startdatecn TEXT,
    countryname TEXT,
    playname TEXT,
    medal INTEGER,
    totalurl TEXT,
    countryid TEXT
);
CREATE INDEX country_awards_countryid_countryname_index ON country_awards (countryid, countryname);"""
        return sql