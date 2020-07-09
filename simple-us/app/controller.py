from typing import List

import ipywidgets
from ipywidgets import Box
from ipymaterialui import Container

from create import CreateTab
from manage import ManageTab
from model import Experiment
from utils import CustomText
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR
from utils import PRIMARY_COLOR_DARK
from view import ViewTab


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
        return Container(children=[self.appview])

    def view_experiments(self, experiments: List[Experiment]):
        print("Navigating")
        self.view_tab.new_view(experiments)
        self.appview.tabs.value = self.view_tab.view


if __name__ == "__main__":
    App()
