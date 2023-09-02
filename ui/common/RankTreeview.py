from ui.utils.TreeviewUtils import TreeViewUtils
from utils.make_image import make_image
from response.rank import MedalRankData
from typing import List
from copy import deepcopy
import tkinter as tk
from utils.GlobalStatic import GlobalResources
from models.enums import Column

class RankTreeview(TreeViewUtils):
    __data : List = []
    __static = GlobalResources()
    def __init__static_data(self):
        self.gold_img = self.__static['gold_img']
        self.silver_img = self.__static['silver_img']
        self.bronze_img = self.__static['bronze_img']
        self.__custom_headings = {
            "#0": {"text": "排名", "anchor": tk.CENTER},
            "#1": {"text": "国家/地区", "anchor": tk.CENTER},
            "#2": {"text": "金牌", "anchor": tk.CENTER, "image": self.gold_img},
            "#3": {"text": "银牌", "anchor": tk.CENTER, "image": self.silver_img},
            "#4": {"text": "铜牌", "anchor": tk.CENTER, "image": self.bronze_img},
            "#5": {"text": "总数", "anchor": tk.CENTER}
            }

        self.__custom_columns = {
            "#0": {"minwidth": 10, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#1": {"minwidth": 20, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#2": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#3": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#4": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'},
            "#5": {"minwidth": 5, "width": 100, "stretch": tk.YES, "anchor": 'center'}
            }

    def __init__(self, parent):
        self.__init__static_data()
        self.__static = GlobalResources()
        super(RankTreeview, self).__init__(parent = parent,
                                              columns = ("排名", "国家/地区", "金牌", "银牌", "铜牌"),
                                              custom_headings = self.__custom_headings,
                                              custom_columns = self.__custom_columns,
                                              show = "tree headings",
                                              )

    @property
    def data(self):
        return deepcopy(self.__data)

    def setup_image(self, Node : List[MedalRankData]):
        [setattr(self, val.countryid, make_image(val.flag)) for val in Node]

    def __insert(self, medal_node):
        flag = self.__static['flags'].get(medal_node.countryid, None)
        self.insert_data(values = (medal_node.countryname,
                                   medal_node.gold,
                                   medal_node.silver,
                                   medal_node.bronze,
                                   medal_node.count),
                         text = (medal_node.rank),
                         image = flag)


    def insert_manny(self, dataList : List[MedalRankData]):
        [self.__insert(medal_node) for medal_node in dataList]
        self.__data = dataList

    def insert_single(self, medal_node):
        self.__insert(medal_node)
        self.__data.append(medal_node)

