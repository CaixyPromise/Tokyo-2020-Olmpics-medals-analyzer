from dataclasses import dataclass, field, asdict, astuple

@dataclass
class RewardRecordResponse:
    __tablename__ = 'reward_record'
    race_id: str
    race_name: str
    file_path : str = field(init=False)

    def __post_init__(self):
        self.file_path = f'static/video/{self.race_id}_{self.race_name}'

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)


@dataclass
class MedalLogResponse:
    race_id: str
    race_name: str
    gold_country_code: str
    gold_player_id: str
    silver_country_code: str
    silver_player_id: str
    bronze_country_code: str
    bronze_player_id: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)