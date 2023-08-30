from dataclasses import dataclass, fields, astuple, asdict, field

@dataclass
class MedalRankData:
    flag : str = field(init=False)
    rank : int
    countryname : str
    countryid : str
    gold : int
    silver : int
    bronze : int
    count : int

    def __post_init__(self):
        self.flag = f'static/image/flags/{self.countryid}.png' if self.countryid else None

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]