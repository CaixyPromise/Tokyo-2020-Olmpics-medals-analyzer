from dataclasses import dataclass, field, asdict, astuple

@dataclass
class SignUpRace:
    __tablename__ = 'signUp_race'
    race_id: int
    player_id: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)