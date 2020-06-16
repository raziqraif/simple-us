from ipymaterialui import Html
from ipymaterialui import Container
from ipywidgets import HBox
from ipywidgets import VBox
from ipywidgets import Layout

from .table import ExperimentTable
from utils import CustomText


class ManageTabView(Container):
    def __init__(self, controller):
        super(Container, self).__init__()

        self.style_ = {"width": "100%", "height": "100%"}

        instruction_text = "Select 1 experiment to display or 2 experiments to compare."
        self.instruction = CustomText(instruction_text,
                                      style_={
                                          "padding": "20px 0px 20px 0px"
                                      },
                                      tag="div")
        self.instruction_bar = HBox(children=[self.instruction],
                                    layout=Layout(width="100%"))
        self.table = ExperimentTable().view
        self.children = [self.instruction_bar, self.table]

        self.controller = controller


class ManageTab:
    def __init__(self):
        self.view = ManageTabView(self)
