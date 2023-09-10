from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column
from response.reward import RewardRecordResponse

class RewardTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(RewardTreeview, self).__init__(parent = parent,
                                           columns = Column.reward.value,
                                           show = 'headings',
                                           column_width = 150)

    def insert_single(self, reward_node : RewardRecordResponse):
        super(RewardTreeview, self).insert_data(values = (reward_node.race_id,
                                                        reward_node.race_name))

    def insert_manny(self, team_nodes : list):
        [self.insert_single(team_node) for team_node in team_nodes]
