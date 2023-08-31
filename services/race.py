from db.DatabaseConnection import DatabaseConnection
from models.medal_Rank import Medal_rank
from response.rank import MedalRankData

class RaceService(DatabaseConnection):
    __tablename__ = "medal_rank"

    def __init__(self) -> None:
        super(RaceService, self).__init__()