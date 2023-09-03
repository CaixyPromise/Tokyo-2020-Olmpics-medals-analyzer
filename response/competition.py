from dataclasses import dataclass, asdict, fields, astuple, field

@dataclass
class CompetitionsResponse:
    __tablename__ = 'competitions'
    competition_id: str = field(default = '')
    time: str = field(default = '')
    main_event: str = field(default = '')  # 比赛大项
    competition_name: str = field(default = '')
    venue: str = field(default = '')  # 比赛地点
    competition_type: str = field(default = '')  # 比赛类型
    status: str = field(default = '')

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]