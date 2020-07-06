from typing import List

from .sidebar import Sidebar
from model import Experiment


class ViewTab:
    def __init__(self):
        from .view import ViewTabUI
        self.sidebar = Sidebar()
        self.view = ViewTabUI(self, self.sidebar.view)
        self.experiments: List[Experiment] = []

    def refresh_sidebar(self):
        self.sidebar.experiments = self.experiments
        self.sidebar.refresh()
