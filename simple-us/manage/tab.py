from ipywidgets import Box

from .table import ExperimentTable


class ManageTabView(Box):
    def __init__(self, controller):
        super(Box, self).__init__()
        self.table = ExperimentTable().view
        self.children = [self.table]


class ManageTab:
    def __init__(self):
        self.view = ManageTabView(self)
