from response.medal import MedalRaceInfo
from ui.utils.TreeviewUtils import TreeViewUtils
from models.enums import Column  # 请确保在这里定义了MedalRaceInfo相关的列
from typing import List, Optional

class MedalRaceInfoTreeview(TreeViewUtils):
    def __init__(self, parent):
        super(MedalRaceInfoTreeview, self).__init__(parent,
                                                    columns=Column.medal_race_info.value,
                                                    show='headings')

    def insert_single(self, response: MedalRaceInfo):
        super(MedalRaceInfoTreeview, self).insert_data(values=response.to_tuple())

    def insert_many(self, response_list: List[Optional[MedalRaceInfo]]):
        [self.insert_single(response) for response in response_list if response is not None]
