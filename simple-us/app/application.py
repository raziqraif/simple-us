from __future__ import annotations

import ipymaterialui as mui
from ipymaterialui import Html
from ipymaterialui import Tab
from ipymaterialui import Tabs
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipywidgets import jslink
# from ipywidgets import Tab
from ipywidgets import VBox
from IPython.display import display

from manage import ManageTab
from manage import ManageTabView


class AppView(widgets.VBox):
    """ View class for the main application """

    def __init__(self, controller: App, create_page, manage_page, view_page, about_page):
        super(Box, self).__init__()

        self.style_ = {
            "width": "100%",
            "height": 20000
        }

        self.controller = controller
        self.create = create_page
        self.manage = manage_page
        self.view = view_page
        self.about = about_page

        self.tabs = Tabs(children=[
            Tab(label="Create", value=self.create),
            Tab(label="Manage", value=self.manage),
            Tab(label="View", value=self.view),
            Tab(label="About", value=self.about),
        ], centered=True, value=self.create)

        self.tab_div = Html(tag="div")
        jslink((self.tabs, 'value'), (self.tab_div, 'children'))

        self.children = [self.tabs, self.tab_div]


class App:
    """ Controller class for AppView """

    def __init__(self):
        self.create = Box()
        self.manage = ManageTab().view
        self.view = Box()
        self.about = Box()

        self.view = AppView(self, self.create, self.manage, self.view, self.about)

        # TODO: Remove this line after manage page is finished
        # self.view.selected_index = 1
        display(self.view)
