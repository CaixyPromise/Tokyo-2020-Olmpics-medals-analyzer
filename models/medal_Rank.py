from db.DatabaseConnection import  DatabaseConnection

class Medal_Rank:
    rank : int
    countryname : str
    countryid : str
    gold : int
    silver : int
    bronze : int
    count : int
    id : int

    def __init__(self, rank = None,
                 countryname = None,
                 countryid = None,
                 gold = None,
                 silver = None,
                 bronze = None, count = None, _id = None):
        self.rank = rank
        self.countryname = countryname
        self.countryid = countryid
        self.gold = gold
        self.silver = silver
        self.bronze = bronze
        self.count = count
        self.id = _id

    def create_table(self):
        sql = """create table medal_rank
(
    rank        INTEGER not null,
    countryname TEXT,
    countryid   TEXT,
    gold        INTEGER,
    silver      INTEGER,
    bronze      INTEGER,
    count       INTEGER,
    id          INTEGER not null
        primary key autoincrement
        unique
);

create index medal_rank_countryid_index
    on medal_rank (countryid);"""
        return sql

