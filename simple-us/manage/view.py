from copy import copy

import ipymaterialui as mui
from ipymaterialui import Button
from ipymaterialui import Chip
from ipymaterialui import Container
from ipymaterialui import Html
from ipymaterialui import Icon
from ipymaterialui import IconButton

from utils.misc import SECONDARY_COLOR, BUTTON_COLOR
from .table import ExperimentTableView
from .controller import ManageTab
import manage
from utils import ExperimentChip
from utils import CustomText
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR


class ManageTabView(Container):
    def __init__(self, controller: ManageTab, experiment_table: ExperimentTableView):
        super(Container, self).__init__()

        self.tag = "div"
        self.style_ = {
                       "padding": "40px 64px 40px 64px",
                       "display": "flex",
                       "flex-direction": "column",
                       "background": MAIN_BACKGROUND_COLOR,
                       }

        self.controller: manage.ManageTab = controller

        self.top_bar = None
        self.table = experiment_table
        self.bottom_bar = None

        self._build_top_bar()
        self._build_bottom_bar()
        self.children = [self.top_bar,
                         self.table,
                         self.bottom_bar]

    def _build_top_bar(self):
        instruction_text = "Select 1 experiment to display or 2 experiments to compare."
        instruction_label = CustomText("Instruction:",
                                       style_={
                                           "font-weight": "bold",
                                           "padding": "0px 8px 0px 0px",
                                   })
        instruction = CustomText(instruction_text, style_={"display": "flex", "flex-grow": "1"})
        refresh_icon = Icon(children="refresh", style_={
            "color": "white",
            "font-size": "20px",
            "padding": "0px 0px 0px 0px",
            "margin": "0px 0px 0px 8px",
        })
        refresh_button = self._create_button("Refresh", icon=refresh_icon, background=PRIMARY_COLOR)
        refresh_button.on_event("onClick", self.controller.onclick_refresh)
        self.top_bar = Container(children=[instruction_label, instruction, refresh_button],
                                 style_={
                                     "padding": "0px 0px 0px 0px",
                                     "margin": "0px 0px 16px 0px",
                                     "display": "flex",
                                     "align-items": "center",
                                     "flex-direction": "row"
                                 })

    def _build_bottom_bar(self):
        text = CustomText("Selected widgets:",
                          style_={
                              "font-weight": "bold",
                              "padding": "0px 0px 0px 0px",
                              "white-space": "nowrap",
                          })

        self.chips_wrapper = Container(children=[],
                                       style_={
                                           "display": "flex",
                                           "flex-direction": "row",
                                           "padding": "0px 0px 0px 8px",
                                       })

        display = self._create_button("Display")
        compare = self._create_button("Compare")

        display.on_event("onClick", self.controller.onclick_display)
        compare.on_event("onClick", self.controller.onclick_compare)

        buttons_wrapper = Container(children=[display, compare],
                                    tag="div",
                                    style_={
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "space-between",
                                        "width": "420px",
                                        "padding": "0px 0px 0px 0px",
                                    })

        self.bottom_bar = Container(children=[text, self.chips_wrapper, buttons_wrapper],
                                    tag="div",
                                    style_={
                                        # "width": "100%",
                                        "height": "35px",
                                        "padding": "0px 0px 0px 0px",
                                        "margin": "24px 0px 0px 0px",
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "align-items": "center",
                                        "justify-content": "flex-start",
                                    })

    def _create_button(self, text, icon: Icon = None, background: str = SECONDARY_COLOR, width: int = 135) -> Button:
        html_text = CustomText(text,
                               style_={
                                   "font-size": "13px",
                                   "color": "#ffffff",
                                   "align-self": "center",
                               })
        children = [html_text] if icon is None else [html_text, icon]
        button = Button(children=children,
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "width": "{}px".format(width),
                            "height": "34px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "0px 0px 0px 8px",
                            "background": background,
                        },)
        return button

    def append_chip(self, experiment_id, experiment_name: str) -> Chip:
        chip = ExperimentChip(experiment_id, experiment_name, style_={"margin": "0px 5px 0px 0px"})
        chip.on_event("onDelete", self.controller.ondelete_chip)

        # It seems like the changes will only take into effect in the frontend if we reassign a new object (with a new
        # memory location) to <widgets>.children
        children = copy(self.chips_wrapper.children)
        children.append(chip)
        self.chips_wrapper.children = children
        return chip

    def remove_chip(self, experiment_id):
        children = copy(self.chips_wrapper.children)
        for ch in children:
            if ch.experiment_id_str == experiment_id:
                children.remove(ch)
                break
        self.chips_wrapper.children = children
