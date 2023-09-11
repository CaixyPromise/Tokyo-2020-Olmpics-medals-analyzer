from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column
from response.competition import RaceTeamInfo
from typing import List, Optional

class RaceTeamTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(RaceTeamTreeview, self).__init__(parent,
                                           columns = Column.race_team_info.value,
                                           show = 'headings'
                                           )

    def insert_single(self, response : RaceTeamInfo):
        super(RaceTeamTreeview, self).insert_data(values = response.to_tuple())

    def insert_manny(self, response : List[RaceTeamInfo]):
        [self.insert_single(r) for r in response]