import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipywidgets import Tab
from ipyleaflet import Map, ImageOverlay, Marker
from manage import ManageTab
from manage import ManageTabView
from IPython.display import display

from ipymaterialui import Tab
from ipymaterialui import Tabs

class AppView(Tabs):
    """ View class for the main application """

    def __init__(self, controller):
        super(Tabs, self).__init__()

        self.value = 0
        self.centered = True
        self.controller = controller

        # TODO: Replace these with proper widgets.
        self.create = Box()
        self.manage = ManageTab().view
        self.view = Box()
        self.about = Box()

        self.children = [
            Tab(label="Create", children=[self.create]),
            Tab(label="Manage", children=[self.manage]),
            Tab(label="View", children=[self.view]),
            Tab(label="About", children=[self.about]),
            # self.manage
            # self.create,
            # self.experiment,
            # self.view,
            # self.about
        ]

        # self.set_title(0, "Create")
        # self.set_title(1, "Manage")
        # self.set_title(2, "View")
        # self.set_title(3, "About")


class App:
    """ Controller class for AppView """

    def __init__(self):
        self.view = AppView(self)

        # TODO: Remove this after manage page is finished
        self.view.selected_index = 1
        display(self.view)

