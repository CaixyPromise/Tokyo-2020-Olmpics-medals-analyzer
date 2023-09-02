from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column

class RaceTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(RaceTreeview, self).__init__(parent = parent,
                                           columns = Column.race.value,
                                           show = 'headings',
                                           )

    def insert_single(self, race_node):
        super(RaceTreeview, self).insert_data(values = (race_node.competition_id,
                                                          race_node.time,
                                                  race_node.main_event,
                                                  race_node.competition_name,
                                                  race_node.venue,
                                                  race_node.competition_type,
                                                  race_node.status))

    def insert_manny(self, race_nodes):
        [self.insert_single(race_node) for race_node in race_nodes]


