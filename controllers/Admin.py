from ui.AdminWindow import AdminDialogWindow
from typing import List, Optional
from response.rank import MedalRankData
from services.medal_rank import MedalRankService
from utils.make_image import make_image
import tkinter as tk
class AdminWindow(AdminDialogWindow):

    def add_image2Attr(self, name, image):
        setattr(self, name, make_image(image))
    def setup_image(self, Node : List[MedalRankData]):
        [self.add_image2Attr(val.countryid, val.flag) for val in Node]

    def __init__(self, master, UserInfo, **kwargs):
        super().__init__(master, **kwargs)
        self.__medal_rank = MedalRankService()
        self.init_medalRank()

    def init_medalRank(self):
        result = self.__medal_rank.query_all_rank()
        self.setup_image(result)
        for dataNode in result:
            self.goldRank_tree.insert('', tk.END,
                                      text = (dataNode.rank),
                                      image = getattr(self, dataNode.countryid),
                                      values = (dataNode.countryname,
                                             dataNode.gold,
                                             dataNode.silver,
                                             dataNode.bronze,
                                             dataNode.count)
                                      )
        # self.setup_image(self.__medal_rank.query_all_rank())