import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipywidgets import jslink
from ipywidgets import Layout
from ipywidgets import VBox
from IPython.display import display

from manage import ManageTab
from manage import ManageTabView
from IPython.display import display


class AppView(Tab):
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

        # TODO: Remove this line after manage page is finished
        self.view.tabs.value = self.manage
        display(self.view)

