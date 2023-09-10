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