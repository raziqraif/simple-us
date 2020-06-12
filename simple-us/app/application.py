from __future__ import annotations

import ipymaterialui as mui
from ipymaterialui import Html
from ipymaterialui import Tab
from ipymaterialui import Tabs
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipywidgets import jslink
from ipywidgets import Layout
from ipywidgets import VBox
from IPython.display import display

from manage import ManageTab
from manage import ManageTabView


class AppView(widgets.VBox):
    """ View class for the main application """

    def __init__(self, controller: App, create_page, manage_page, view_page, about_page):
        super(Box, self).__init__()

        self.layout.width = "100%"
        self.layout.height = "900px"
        self.layout.display = "flex"
        self.layout.flex_direction = "row"
        self.layout.flex_wrap = "wrap"
        self.layout.justify_content = "flex-start"
        self.layout.align_items = "center"

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
        self.view.tabs.value = self.manage
        display(self.view)

