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

        self.style_ = {"width": "100%",
                       "height": "100%",
                       "padding": "0px 50px 0px 50px",
                       }

        instruction_text = "Select 1 experiment to display or 2 experiments to compare."
        self.instruction_label = CustomText("Instruction:",
                                            style_={
                                                "font-weight": "bold",
                                                "padding": "0px 5px 0px 0px"
                                            })
        self.instruction = CustomText(instruction_text)
        self.instruction_bar = Container(children=[self.instruction_label, self.instruction],
                                         style_={
                                             "width": "100%",
                                             "padding": "30px 0px 12px 0px",
                                             "display": "flex",
                                             "flex-direction": "row"
                                         })
        self.table = ExperimentTable().view
        self.children = [self.instruction_bar, self.table]

        self.controller = controller


class ManageTab:
    def __init__(self):
        self.view = ManageTabView(self)
