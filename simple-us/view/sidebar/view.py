from copy import copy
from typing import List

from ipymaterialui import Button
from ipymaterialui import Container
from ipymaterialui import FormControl
from ipymaterialui import FormControlLabel
from ipymaterialui import Html
from ipymaterialui import Input
from ipymaterialui import InputLabel
from ipymaterialui import MenuItem
from ipymaterialui import Select
from ipymaterialui import Slider
from ipymaterialui import TextField
from ipymaterialui import TextareaAutosize
import ipywidgets as widgets
from ipywidgets import Layout

from .controller import Sidebar
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR

WIDGET_LEN = "220px"


class SidebarView(Container):

    def __init__(self, controller: Sidebar, **kwargs):
        super().__init__(**kwargs)

        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "align-self": "center",
            "padding": "32px 32px 32px 32px",
            "width": "290px",
            "height": "600px",
            "margin": "0px 0px 0px 0px",
            # "border-radius": "8px",
            "border": "1px solid " + PRIMARY_COLOR,
            # "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller

        self.title = CustomText("Variables", style_={"font-weight": "bold",
                                                     "font-size": "16px",
                                                     "margin": "0px 0px 24px 0px"})
        self.system_components = None
        self.spatial_resolution = None
        self.type_of_results = None
        self.result_to_view = None
        self.filter = None
        self.buttons_wrapper = None

        self.build_system_components()
        self.build_spatial_resolution()
        self.build_type_of_results()
        self.build_result_to_view()
        self.build_filter()
        self.build_buttons_wrapper()

        self.children = [self.title, self.system_components, self.spatial_resolution, self.type_of_results,
                         self.result_to_view, self.filter, self.buttons_wrapper]

    def build_system_components(self):
        text = CustomText("System Components", style_={"font-weight": "bold"})
        options: List[str] = self.controller.system_components()
        assert "" in options
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, select])
        self.system_components = wrapper

    def build_spatial_resolution(self):
        text = CustomText("Spatial Resolution", style_={"font-weight": "bold"})
        options: List[str] = self.controller.spatial_resolution()
        assert "" in options
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, select])
        self.spatial_resolution = wrapper

    def build_type_of_results(self):
        text = CustomText("Type Of Results", style_={"font-weight": "bold"})
        options = self.controller.type_of_results()
        assert "" in options
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, select])
        self.type_of_results = wrapper

    def build_result_to_view(self):
        text = CustomText("Result To View", style_={"font-weight": "bold"})
        options = self.controller.result_to_view()
        assert "" in options
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, select])
        self.result_to_view = wrapper

    def build_filter(self):
        text = CustomText("Filter", style_={"font-weight": "bold"})
        # material ui's slider crashes when the user moves the it too quickly
        # slider = Slider(value=[0, 100], max=100.0, min=0.00, step=0.05, marks=[0, 20, 40, 60, 80, 100])
        # layout = Layout(width="180px", margin="8px 8px 0px 8px", align_items="center")
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px", align_items="center")
        slider = widgets.FloatRangeSlider(
            value=[0, 100], min=0, max=100, step=0.05, continuous_update=False, readout=False,
            layout=layout,
        )
        zero = CustomText("0%")
        hundred = CustomText("100%")
        # slider_wrapper = Container(children=[zero, slider, hundred],
        #                            style_={
        #                                "display": "flex",
        #                                "flex-direction": "row",
        #                                "justify-content": "center",
        #                                "align-items": "center",
        #                                "padding": "0px 0px 0px 0px",
        #                                "width": "auto",
        #                            })
        wrapper = self._create_input_wrapper([text, slider])
        self.filter = wrapper

    def build_buttons_wrapper(self):
        visualize = self._create_button("Visualize")
        csv = self._create_button("CSV")
        wrapper = self._create_input_wrapper([visualize, csv])
        style_ = copy(wrapper.style_)
        style_["margin"] = "32px 12px 32px 12px"
        wrapper.style_ = style_
        self.buttons_wrapper = wrapper

    def _create_button(self, text: str) -> Button:
        text_html = CustomText(text,
                               style_={
                                   "display": "flex",
                                   "align-items": "center",
                                   "font-size": "12px",
                                   "color": "#ffffff",
                                   "align-self": "center",
                               })
        button = Button(children=[text_html],
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "display": "flex",
                            "width": WIDGET_LEN,
                            "height": "35px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "4px 0px 4px 0px",
                            "background": PRIMARY_COLOR,
                            "align-items": "center !important",
                        }, )
        return button

    def _create_input_wrapper(self, children: List[any]) -> Container:
        wrapper = Container(children=children,
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                                "width": WIDGET_LEN,
                                "margin": "4px 12px 4px 12px",
                                "padding": "0px 0px 0px 0px",
                            })
        return wrapper
