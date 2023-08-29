from ui.AdminWindow import AdminDialogWindow

class AdminWindow(AdminDialogWindow):

    def __init__(self, master, UserInfo, **kwargs):
        super().__init__(master, **kwargs)
        self.init_medalRank()

    def init_medalRank(self):
        pass