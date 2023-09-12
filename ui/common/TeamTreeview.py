from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column
from utils.GlobalStatic import GlobalResources
from models.team import NationalTeam

class TeamTreeview(TreeViewUtils):
    __static = GlobalResources()
    # ('国家名称', '国家代码', '团队总人数', '管理员名称', '管理员联系方式', '管理员身份')
    def __init__(self, parent):
        self.__custom_headings = {
            "#0": {"text": "国家代码", "anchor": 'center'},
            "#1": {"text": "国家名称", "anchor": 'center'},
            "#2": {"text": "团队总人数", "anchor": 'center'},
            "#3": {"text": "管理员名称", "anchor": 'center'},
            "#4": {"text": "管理员联系方式", "anchor": 'center'},
            "#5": {"text": "管理员身份", "anchor": 'center'}
            }

        self.__custom_columns = {
            "#0": {"minwidth": 20, "width": 100, "stretch": 1, "anchor": 'center'},
            "#1": {"minwidth": 10, "width": 100, "stretch": 1, "anchor": 'center'},
            "#2": {"minwidth": 5, "width": 125, "stretch": 1, "anchor": 'center'},
            "#3": {"minwidth": 5, "width": 120, "stretch": 1, "anchor": 'center'},
            "#4": {"minwidth": 5, "width": 150, "stretch": 1, "anchor": 'center'},
            "#5": {"minwidth": 5, "width": 125, "stretch": 1, "anchor": 'center'}
            }
        super(TeamTreeview, self).__init__(parent = parent,
                                           columns = ('国家代码', '国家名称', '团队总人数', '管理员名称', '管理员联系方式', ),
                                           custom_columns = self.__custom_columns,
                                           custom_headings = self.__custom_headings,
                                           show = 'tree headings'
                                           )

    def insert_single(self, team_node : NationalTeam):
        flag = self.__static['flags'].get(team_node.country_code, None)
        super(TeamTreeview, self).insert_data(values = (
            team_node.country_name,
            team_node.team_size,
            team_node.manager_name,
            team_node.manager_contact,
            team_node.manager_identity,
        ),
                text = team_node.country_code,
                image = flag
                )

    def insert_manny(self, team_nodes : list):
        [self.insert_single(team_node) for team_node in team_nodes]
