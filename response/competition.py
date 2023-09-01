from dataclasses import dataclass, asdict, fields, astuple

@dataclass
class CompetitionsData:
    __tablename__ = 'competitions'
    competition_id: str
    time: str
    main_event: str
    competition_name: str
    venue: str
    status: str

    def to_tuple(self):
        return astuple(self)

    def to_dict(self):
        return asdict(self)

    def to_list(self):
        return [getattr(self, f.name) for f in fields(self)]