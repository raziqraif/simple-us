from __future__ import annotations

from ipymaterialui import Container
from ipymaterialui import Html
from ipymaterialui import Tab
from ipymaterialui import Tabs
import ipywidgets
from ipywidgets import Box
from ipywidgets import jslink
from IPython.display import display

from create import CreateTab
from manage import ManageTab
from utils import CustomText
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR
from utils import PRIMARY_COLOR_DARK
from view import ViewTab

TAB_HEIGHT = "60px"


class AppView(Container):
    """ View class for the main application """

    def __init__(self, controller: App, create_page, manage_page, view_page, about_page):
        super(Container, self).__init__()
        self.style_ = {
            # "width": "933px",
            # "width": "100% !important",
            # "width": "2000px",
            "margin": "0px 0px 16px 0px",
            # "padding": "0px 0px 0px 0px",
            # "display": "flex",
            # "flex-direction": "column",
            "background": MAIN_BACKGROUND_COLOR,
            # "align-items": "stretch",
            # "align-self": "center",
        }

        self.controller = controller
        self.create = create_page
        self.manage = manage_page
        self.view = view_page
        self.about = about_page

        self.tabs = Tabs(
            children=[
                Tab(label=CustomText("Create",
                                     style_={
                                         "color": "#ffffff",
                                         # "height": TAB_HEIGHT,
                                     }), value=self.create),
                Tab(label=CustomText("Manage",
                                     style_={
                                         "color": "#ffffff",
                                         # "height": TAB_HEIGHT,
                                     }), value=self.manage),
                Tab(label=CustomText("View",
                                     style_={
                                         "color": "#ffffff",
                                         # "height": TAB_HEIGHT,
                                     }), value=self.view),
                Tab(label=CustomText("About",
                                     style_={
                                         "color": "#ffffff",
                                         # "height": TAB_HEIGHT,
                                     }), value=self.about),
            ],
            style_={
                "background": PRIMARY_COLOR,
                "height": "65px",
                "display": "flex",
                "flex-direction": "row",
                "align-items": "center",
            },
            centered=True, value=self.create
        )

        self.tab_div = Html(tag="div",
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": "stretch",
                                "height": "810px",
                                "padding": "0px 0px 0px 0px",
                                "background": MAIN_BACKGROUND_COLOR,
                                "border": "1px solid " + PRIMARY_COLOR,
                            })
        jslink((self.tabs, 'value'), (self.tab_div, 'children'))

        self.children = [self.tabs, self.tab_div]


class App:
    """ Controller class for AppView """

    def __init__(self):
        self.create_tab: CreateTab = CreateTab()
        self.manage_tab: ManageTab = ManageTab()
        self.view_tab: ViewTab = ViewTab()
        self.about_tab = Box()

        self.view = AppView(self,
                            self.create_tab.view,
                            self.manage_tab.view,
                            self.view_tab.view,
                            self.about_tab)
        self.view.tabs.value = self.manage_tab.view

    def display(self):
        return Container(children=self.view)


if __name__ == "__main__":
    App()
