from dataclasses import dataclass, fields, asdict, astuple, field

@dataclass
class UserConfig:
    id_ : int
    username : str
    role: int
    group_id: str
    public_userid: str
    user_contact : str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class UserResponse:
    username : str
    public_userid : str
    user_contact : str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class UserDeleteResponse:
    public_userid : str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class UserAddAdminResponse:
    username: str
    public_userid: str
    user_contact: str
    role: int = field(default = -1, )
    group_id: str = field(default = '')
    password_hash: str = field(default = '')

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class UserModifyResponse:
    username : str
    public_userid : str
    user_contact : str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class InsertPlayerResponse:
    username: str
    public_userid: str
    user_contact : str
    group_id: str
    role: int = field(default = 2)
    password_hash: str = field(default = '123456')

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]