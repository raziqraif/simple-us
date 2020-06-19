from __future__ import annotations
from copy import copy

import ipymaterialui as mui
from ipymaterialui import Button
from ipymaterialui import Chip
from ipymaterialui import Container
from ipymaterialui import Icon
from ipymaterialui import IconButton

import manage
from .table import ExperimentTableView
from utils import ExperimentChip
from utils import CustomText


class ManageTabView(Container):
    def __init__(self, controller: manage.ManageTab, experiment_table: ExperimentTableView):
        super(Container, self).__init__()

        self.style_ = {"width": "100%",
                       "height": "850px",
                       "padding": "0px 50px 0px 50px",
                       "display": "flex",
                       "flex-direction": "column",
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
                                           "padding": "0px 5px 0px 0px"
                                       })
        instruction = CustomText(instruction_text)
        self.top_bar = Container(children=[instruction_label, instruction],
                                 style_={
                                     "width": "100%",
                                     "padding": "30px 0px 20px 0px",
                                     "display": "flex",
                                     "flex-direction": "row"
                                 })

    def _build_bottom_bar(self):
        text = CustomText("Selected widgets:",
                          style_={
                              "font-weight": "bold",
                              "padding": "0px 0px 0px 0px",
                              "white-space": "nowrap",
                              "align-self": "center",
                          })

        self.chips_wrapper = Container(children=[],
                                       style={
                                            "padding": "0px 0px 0px 0px",
                                            # "display": "flex",
                                            # "flex-direction": "row"
                                        })

        display = self._create_button("Display")
        compare = self._create_button("Compare")

        buttons_wrapper = Container(children=[display, compare],
                                    style={
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "flex-end",
                                        "flex": 1,
                                        "width": "100%",
                                        "padding": "0px 0px 0px 0px",
                                    })

        self.bottom_bar = Container(children=[text, self.chips_wrapper, buttons_wrapper],
                                    style_={
                                        "width": "100%",
                                        "height": "35px",
                                        "padding": "40px 0px 0px 0px",
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "align-items": "center",
                                        "justify-content": "flex-start",
                                        # "flex": 1,
                                    })

    def _create_button(self, text) -> Button:
        button = Button(children=CustomText(text,
                                            style_={
                                                "font-size": "13px",
                                                "color": "#ffffff",
                                                "align-self": "center",
                                            }),
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "width": "140px",
                            "background": "#454851",
                        },)
        return button

    def append_chip(self, experiment_id, experiment_name: str) -> Chip:
        chip = ExperimentChip(experiment_id, experiment_name)
        chip.on_event("onDelete", self.controller.ondelete_chip)

        children = copy(self.chips_wrapper.children)
        children.append(chip)
        self.chips_wrapper.children = children
        return chip

    def remove_chip(self, experiment_id):
        children = copy(self.chips_wrapper.children)
        for ch in children:
            if ch.experiment_id == experiment_id:
                children.remove(ch)
                break
        self.chips_wrapper.children = children
