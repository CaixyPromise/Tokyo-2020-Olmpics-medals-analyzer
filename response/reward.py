from dataclasses import dataclass, field, asdict, astuple

@dataclass
class RewardRecordResponse:
    __tablename__ = 'reward_record'
    race_id: str
    race_name: str
    file_path = ''

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)