from enum import Enum, unique

@unique
class ColumnName(Enum):
    race = '比赛'
    team = '队伍'
    medal = '奖牌榜'
    admin = '管理员'
    player = '我的比赛'
    reward = '精彩时刻'
    medal_log = '奖牌榜日志'

@unique
class Column(Enum):
    race = ("比赛ID", "时间", '比赛大项', "比赛名称", "比赛场馆",  "比赛类型", '比赛状态')
    team = ('国家代码', '国家名称', '团队总人数', '管理员名称', '管理员联系方式', '管理员身份')
    medal = ("排名", "国家/地区", "国家/地区代码","金牌", "银牌", "铜牌", '总数')
    admin = ('管理员账号', '管理员名称', '管理员联系方式')
    player = ('运动员账号', '运动员名称', '运动员联系方式')
    reward = ('比赛ID', '比赛名称')
    medal_log = ('比赛ID', '比赛名称', '金牌国家代码', '金牌运动员ID',
                 '银牌国家代码', '银牌运动员ID',
                 '铜牌国家代码',
                 '铜牌运动员ID')

