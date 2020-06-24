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
from ipymaterialui import TextField
from ipymaterialui import TextareaAutosize
import ipywidgets as widgets
from ipywidgets import FileUpload
from ipywidgets import Layout

from .controller import Sidebar
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR

WIDGET_LEN = "250px"


class SidebarView(Container):

    def __init__(self, controller: Sidebar, **kwargs):
        super().__init__(**kwargs)

        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "align-self": "center",
            "padding": "0px 0px 0px 0px",
            "width": "320px",
            "height": "700px",
            "margin": "0px 0px 60px 0px",
            "border-radius": "8px",
            "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller

        self.system_components = None
        self.spatial_resolution =  None
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

        self.children = [self.system_components, self.spatial_resolution, self.type_of_results,
                         self.result_to_view, self.filter, self.buttons_wrapper]

    def build_system_components(self):
        text = CustomText("Food, Water, Energy System Components")
        options: List[str] = self.controller.system_components()
        assert "" in options
        layout = Layout(width="250px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = Container(children=[text, select],
                            style_={

                            })
        self.system_components = wrapper

    def build_spatial_resolution(self):
        text = CustomText("Spatial Resolution")
        options: List[str] = self.controller.spatial_resolution()
        assert "" in options
        layout = Layout(width="250px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = Container(children=[text, select],
                            style_={

                            })
        self.spatial_resolution = wrapper

    def build_type_of_results(self):
        text = CustomText("Type Of Results")
        options = self.controller.type_of_results()
        assert "" in options
        layout = Layout(width="250px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = Container(children=[text, select],
                            style_={

                            })
        self.type_of_results = wrapper

    def build_result_to_view(self):
        text = CustomText("Result To View")
        options = self.controller.result_to_view()
        assert "" in options
        layout = Layout(width="250px")
        select = widgets.Dropdown(value="", options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, select])
        self.result_to_view = wrapper

    def build_filter(self):
        text = CustomText("Filter")
        wrapper = Container(children=[text],
                            style_={

                            })
        self.filter = wrapper

    def build_buttons_wrapper(self):
        visualize = self._create_button("Visualize")
        csv = self._create_button("CSV")
        wrapper = self._create_input_wrapper([visualize, csv])
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
                            "width": "120px",
                            "height": "30px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "0px 0px 0px 0px",
                            "background": PRIMARY_COLOR,
                            "align-items": "center !important",
                        }, )
        return button

    def _create_input_wrapper(self, children: List[any]) -> Container:
        wrapper = Container(children=children,
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                            })
        return wrapper
