from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column

class AdminTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(AdminTreeview, self).__init__(parent = parent,
                                            columns = Column.admin.value,
                                            show = 'headings')

    def insert_single(self, dataNode):
        super(AdminTreeview, self).insert_data(dataNode.id_,
                                               dataNode.name)

    def insert_manny(self, dataList):
        [self.insert_single(dataNode) for dataNode in dataList]