from enum import Enum, unique

@unique
class ColumnName(Enum):
    race = '比赛'
    team = '队伍'
    medal = '奖牌榜'
    admin = '管理员'

@unique
class Column(Enum):
    race = ['比赛时间', '比赛地点', '比赛名称', '比赛类型','比赛状态']
    team = ['国家名称', '用户账号', '用户姓名', '用户身份',]
    medal = ["排名", "国家/地区", "金牌", "银牌", "铜牌", '总数']
    admin = ['管理员账号', '管理员名称',]


@unique
class AskQuestion(Enum):
    race = dict(zip(['比赛名称', '比赛类型', '比赛时间', '比赛地点', '比赛状态'], ['text', 'text', 'date', 'text', 'text']))
    team = dict(zip(['国家名称', '用户账号', '用户姓名', '用户身份'], ['text', 'text', 'text', 'text']))
    medal = dict(zip(['排名', '国家/地区', '金牌', '银牌', '铜牌', '总数'], ['text', 'text', 'text', 'text', 'text', 'text']))
    admin = dict(zip(['管理员账号', '管理员名称'], ['text', 'text']))

