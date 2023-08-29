from dataclasses import dataclass, fields, asdict, astuple

@dataclass
class UserConfig:
    _id : int
    username : str
    role: int
    group_id: str
    public_userid: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]