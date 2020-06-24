from .sidebar import Sidebar


class ViewTab:
    def __init__(self):
        from .view import ViewTabUI
        self.sidebar = Sidebar()
        self.view = ViewTabUI(self, self.sidebar.view)

