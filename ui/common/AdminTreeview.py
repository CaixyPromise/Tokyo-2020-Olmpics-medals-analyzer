from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column

class AdminTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(AdminTreeview, self).__init__(parent = parent,
                                            columns = Column.admin.value,
                                            show = 'headings',
                                            column_width = 150)

    def insert_single(self, dataNode):
        super(AdminTreeview, self).insert_data(values = (dataNode.public_userid,
                                               dataNode.username,
                                               dataNode.user_contact))

    def insert_manny(self, dataList):
        print(dataList)
        [self.insert_single(dataNode) for dataNode in dataList]