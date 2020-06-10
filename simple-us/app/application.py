import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipywidgets import Tab
from ipyleaflet import Map, ImageOverlay, Marker
from manage import ManageTab
from manage import ManageTabView
from IPython.display import display


class AppView(Tab):
    """ View class for the main application """

    def __init__(self, controller):
        super(Tab, self).__init__()

        self.controller = controller

        # TODO: Replace these with proper widgets.
        self.create = Box()
        self.experiment = ManageTab().view
        self.view = Box()
        self.about = Box()

        self.children = [
            self.create,
            self.experiment,
            self.view,
            self.about
        ]

        self.set_title(0, "Create")
        self.set_title(1, "Manage")
        self.set_title(2, "View")
        self.set_title(3, "About")


class App:
    """ Controller class for AppView """

    def __init__(self):
        self.view = AppView(self)

        # TODO: Remove this after manage page is finished
        self.view.selected_index = 1
        display(self.view)

