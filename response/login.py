from dataclasses import dataclass, asdict, astuple, fields

@dataclass
class LoginVerifyResponse:
    public_id: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class LoginResponse:
    public_id : str
    password  : str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]