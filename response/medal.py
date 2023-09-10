from dataclasses import dataclass, fields, astuple, asdict, field

@dataclass
class MedalInsertResponse:
    race_id : str
    gold_code : str
    gold_player : str
    silver_code : str
    silver_player : str
    bronze_code : str
    bronze_player : str

    def __post_init__(self):
        if (not all(self.to_tuple())):
            raise ValueError("All fields must be non-empty")

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]
