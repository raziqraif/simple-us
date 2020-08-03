from copy import copy
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
from experimentsview import ViewTab
from utils.pubsubmessage import unsubAll, sendMessage, subscribe, REFRESH_BUTTON_CLICKED, NOTIFICATION_CREATED
from utils.widgets.notification import Notification


class App:
    """ Controller class for AppView """

    def __init__(self):
        unsubAll()  # Previous listeners would still be alive even if the kernel has been restarted
        # (probably until the garbage collector kicks in). Unsubscribe them here.

        self.create_tab: CreateTab = CreateTab()
        self.manage_tab: ManageTab = ManageTab(self.view_experiments)
        self.experiments_view_tab: ViewTab = ViewTab()
        self.about_tab = Box()

        self._notification_key = 1

        from app import AppView
        self.view = AppView(self,
                            self.create_tab.view,
                            self.manage_tab.view,
                            self.experiments_view_tab.view,
                            self.about_tab)
        self.view.tabs.value = self.manage_tab.view

        subscribe(self._handle_notification_created, NOTIFICATION_CREATED)

    def display(self):
        SIMPLEUtil.init_working_directory()
        return Container(children=[self.view],
                         style_={"width": "100%",
                                 "maxWidth": "100%",
                                 "display": "flex",
                                 "flex-direction": "row",
                                 "justify-content": "center",
                                 "align-items": "flex-start",
                                 "margin": "0px 0px 0px 56px",
                                 "padding": "0px 0px 0px 0px",
                                 })

    def view_experiments(self, experiment_1: Experiment, experiment_2: Optional[Experiment]) -> bool:
        # Display or compare experiments

        experiments = [experiment_1] if experiment_2 is None else [experiment_1, experiment_2]
        created = self.experiments_view_tab.new_view(experiments)
        if created:
            self.view.tabs.value = self.experiments_view_tab.view
            return True
        return False

    def _handle_notification_created(self, text: str, mode: str, page: str):
        if self._notification_key == 1:
            self._notification_key = 2
            self.view.notification_2.open_ = False
            self.view.notification_1.show(text, mode, page)
        elif self._notification_key == 2:
            self._notification_key = 1
            self.view.notification_1.open_ = False
            self.view.notification_2.show(text, mode, page)


if __name__ == "__main__":
    App()
