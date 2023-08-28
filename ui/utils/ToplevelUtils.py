from  tkinter import Toplevel

class TopLevelUtils(Toplevel):
    def __init__(self, master, geometry, title = '顶部窗口', **kwargs):
        super().__init__(master = master, **kwargs)
        self.title(title)
        self.geometry(geometry)