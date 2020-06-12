from ipymaterialui import Html
from ipywidgets import HBox
from ipywidgets import VBox
from ipywidgets import Layout

from .table import ExperimentTable
from utils import CustomText


class ManageTabView(VBox):
    def __init__(self, controller):
        super(VBox, self).__init__()

        self.layout.width = "1000px"
        self.layout.height = "100%"
        self.layout.display = "flex"
        self.layout.flex_direction = "column"
        self.layout.flex_wrap = "wrap"
        self.layout.justify_content = "center"
        self.layout.align_items = "center"

        instruction_text = "Select 1 experiment to display or 2 experiments to compare."
        self.instruction = CustomText(instruction_text, style_={"font-size": 50}, tag="div")
        self.instruction_bar = HBox(children=[self.instruction],
                                    layout=Layout(width="100%"))
        self.table = ExperimentTable().view
        self.children = [self.instruction_bar, self.table]


class ManageTab:
    def __init__(self):
        self.view = ManageTabView(self)
