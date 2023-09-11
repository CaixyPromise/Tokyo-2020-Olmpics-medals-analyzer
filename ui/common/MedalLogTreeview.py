from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column
from response.reward import MedalLogResponse
from typing import List, Optional

class MedalLogTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(MedalLogTreeview, self).__init__(parent,
                                           columns = Column.medal_log.value,
                                           show = 'headings'
                                           )

    def insert_single(self, response :MedalLogResponse):
        super(MedalLogTreeview, self).insert_data(values = response.to_tuple())

    def insert_manny(self, responseList: List[Optional[MedalLogResponse]]):
        [self.insert_single(response) for response in responseList
         if response is not None]
