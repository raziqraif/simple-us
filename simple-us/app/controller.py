from typing import List, Optional
from typing import Callable

import ipywidgets
from ipywidgets import Box
from ipymaterialui import Container

from create import CreateTab
from manage import ManageTab
from model import Experiment
from utils import CustomText, SIMPLEUtil
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR
from utils import PRIMARY_COLOR_DARK
from experimentsview import ViewTab


class App:
    """ Controller class for AppView """

    def __init__(self):
        self.create_tab: CreateTab = CreateTab()
        self.manage_tab: ManageTab = ManageTab(self.view_experiments)
        self.view_tab: ViewTab = ViewTab()
        self.about_tab = Box()

        from app import AppView
        self.appview = AppView(self,
                               self.create_tab.view,
                               self.manage_tab.view,
                               self.view_tab.view,
                               self.about_tab)
        self.appview.tabs.value = self.view_tab.view

    def display(self):
        SIMPLEUtil.init_working_directory()
        return Container(children=[self.appview])

    def view_experiments(self, experiment_1: Experiment, experiment_2: Optional[Experiment]) -> bool:
        experiments = [experiment_1] if experiment_2 is None else [experiment_1, experiment_2]
        created = self.view_tab.new_view(experiments)
        if created:
            self.appview.tabs.value = self.view_tab.view
            return True
        return False

if __name__ == "__main__":
    App()
