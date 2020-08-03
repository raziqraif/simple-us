from copy import copy
from typing import List, Optional, Tuple

from ipymaterialui import Button, Icon
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
from ipywidgets import Dropdown
from ipywidgets import Layout

from utils.misc import SECONDARY_COLOR
from .controller import Sidebar
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
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
            "height": "640px",
            "margin": "0px 0px 0px 0px",
            # "border-radius": "8px",
            "border": "1px solid " + PRIMARY_COLOR,
            # "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller

        self._title = CustomText("Variables", style_={"font-weight": "bold",
                                                      "font-size": "16px",
                                                      "margin": "0px 0px 24px 0px"})
        self._system_component_wrapper = None
        self._spatial_resolution_wrapper = None
        self._type_of_result_wrapper = None
        self._result_to_view_wrapper = None
        self._filter_wrapper = None
        self._buttons_wrapper = None

        self._system_components_select: Optional[Dropdown] = None
        self._spatial_resolution_select: Optional[Dropdown] = None
        self._type_of_results_select: Optional[Dropdown] = None
        self._result_to_view_select: Optional[Dropdown] = None
        self._filter_title: Optional[CustomText] = None
        self._filter_slider: Optional[widgets.FloatRangeSlider] = None

        self._build_system_components()
        self._build_spatial_resolution()
        self._build_type_of_results()
        self._build_result_to_view()
        self._build_filter()
        self._build_buttons_wrapper()

        self.children = [self._title, self._system_component_wrapper, self._spatial_resolution_wrapper,
                         self._type_of_result_wrapper, self._result_to_view_wrapper, self._filter_wrapper,
                         self._buttons_wrapper]

    def _build_system_components(self):
        text = CustomText("System Components", style_={"font-weight": "bold"})
        options: List[str] = ["Select"]
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        self._system_components_select = widgets.Dropdown(value=options[0], options=options, layout=layout)
        self._system_components_select.observe(self.controller.onchange_system_components)
        wrapper = self._create_input_wrapper([text, self._system_components_select])
        self._system_component_wrapper = wrapper

    def _build_spatial_resolution(self):
        text = CustomText("Spatial Resolution", style_={"font-weight": "bold"})
        options: List[str] = ["Select"]
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        self._spatial_resolution_select = widgets.Dropdown(value=options[0], options=options, layout=layout)
        self._spatial_resolution_select.observe(self.controller.onchange_spatial_resolution)
        wrapper = self._create_input_wrapper([text, self._spatial_resolution_select])
        self._spatial_resolution_wrapper = wrapper

    def _build_type_of_results(self):
        text = CustomText("Type Of Results", style_={"font-weight": "bold"})
        options = ["Select"]
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        self._type_of_results_select = widgets.Dropdown(value=options[0], options=options, layout=layout)
        self._type_of_results_select.observe(self.controller.onchange_type_of_results)
        wrapper = self._create_input_wrapper([text, self._type_of_results_select])
        self._type_of_result_wrapper = wrapper

    def _build_result_to_view(self):
        text = CustomText("Result To View", style_={"font-weight": "bold"})
        options = ["Select"]
        layout = Layout(width=WIDGET_LEN, margin="8px 0px 0px 0px")
        self._result_to_view_select = widgets.Dropdown(value=options[0], options=options, layout=layout)
        wrapper = self._create_input_wrapper([text, self._result_to_view_select])
        self._result_to_view_wrapper = wrapper

    def _build_filter(self):
        text = CustomText("Filter: 0 - 100%", style_={"font-weight": "bold"})
        # material ui's slider crashes when the user moves the it too quickly
        # slider = Slider(value=[0, 100], max=100.0, min=0.00, step=0.05, marks=[0, 20, 40, 60, 80, 100])
        # layout = Layout(width="180px", margin="8px 8px 0px 8px", align_items="center")
        layout = Layout(width=WIDGET_LEN, margin="4px 0px 0px 0px", align_items="center")
        self._filter_slider = widgets.FloatRangeSlider(
            value=[0, 100], min=0, max=100, step=1, continuous_update=False, readout=False,
            layout=layout,
        )
        self._filter_slider.observe(self.controller.onchange_filter_range)
        # zero = CustomText("0%")
        # hundred = CustomText("100%")
        # slider_wrapper = Container(children=[zero, slider, hundred],
        #                            style_={
        #                                "display": "flex",
        #                                "flex-direction": "row",
        #                                "justify-content": "center",
        #                                "align-items": "center",
        #                                "padding": "0px 0px 0px 0px",
        #                                "width": "auto",
        #                            })
        wrapper = self._create_input_wrapper([text, self._filter_slider])
        self._filter_title = wrapper.children[0]
        self._filter_wrapper = wrapper

    def _build_buttons_wrapper(self):
        visualize = self._create_button("Visualize")
        visualize.on_event("onClick", self.controller.onclick_visualize)
        download_icon = Icon(children="cloud_download_outline_blank",
                             style_={
                                 "color": "white",
                                 "font-size": "18px",
                                 "padding": "0px 0px 0px 0px",
                                 "margin": "0px 0px 0px 8px",
                             })
        csv = self._create_button("CSV", icon=download_icon)
        csv.on_event("onClick", self.controller.onclick_csv)
        close = self._create_button("Close", SECONDARY_COLOR)
        close.on_event("onClick", self.controller.onclick_close)
        wrapper = self._create_input_wrapper([visualize, csv, close])
        style_ = copy(wrapper.style_)
        style_["margin"] = "32px 12px 0px 12px"
        wrapper.style_ = style_
        self._buttons_wrapper = wrapper

    def _create_button(self, text: str, background: str = PRIMARY_COLOR, icon: Icon = None) -> Button:
        text_html = CustomText(text,
                               style_={
                                   "display": "flex",
                                   "align-items": "center",
                                   "font-size": "12px",
                                   "color": "#ffffff",
                                   "align-self": "center",
                               })
        children = [text_html] if icon is None else [text_html, icon]
        button = Button(children=children,
                        # color="#454851",
                        color=background,
                        focus_ripple=True,
                        style_={
                            "display": "flex",
                            "width": WIDGET_LEN,
                            "height": "35px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "4px 0px 4px 0px",
                            "background": background,
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

    def update_system_component_options(self, options: List[str]):
        assert "Select" in options
        self._system_components_select.options = options

    def update_spatial_resolution_options(self, options: List[str]):
        assert "Select" in options
        self._spatial_resolution_select.options = options

    def update_type_of_results_options(self, options: List[str]):
        assert "Select" in options
        self._type_of_results_select.options = options

    def update_result_to_view_options(self, options: List[str]):
        assert "Select" in options
        self._result_to_view_select.options = options

    def set_system_component(self, value: str):
        assert value in self._system_components_select.options
        self._system_components_select.value = value

    def set_spatial_resolution(self, value: str):
        assert value in self._spatial_resolution_select.options
        self._spatial_resolution_select.value = value

    def set_type_of_result(self, value: str):
        assert value in self._type_of_results_select.options
        self._type_of_results_select.value = value

    def set_result_to_view(self, value: str):
        self._result_to_view_select.value = value

    def set_filter_range(self, min_: int, max_: int):
        assert 0 <= min_ <= 100
        assert 0 <= max_ <= 100
        assert min_ <= max_

        self._filter_slider.value = (min_, max_)
        self._filter_title.children = "Filter: {} - {}%".format(min_, max_)

    @property
    def system_component(self) -> str:
        return self._system_components_select.value

    @property
    def spatial_resolution(self) -> str:
        return self._spatial_resolution_select.value

    @property
    def type_of_result(self) -> str:
        return self._type_of_results_select.value

    @property
    def result_to_view(self) -> str:
        return self._result_to_view_select.value

    @property
    def filter_range(self) -> Tuple[int, int]:
        min_ = self.filter_min
        max_ = self.filter_max
        return min_, max_

    @property
    def filter_min(self) -> int:
        return int(self._filter_slider.value[0])

    @property
    def filter_max(self) -> int:
        return int(self._filter_slider.value[1])
