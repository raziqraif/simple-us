from copy import copy

from ipyleaflet import Map
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

from .controller import ViewTab
from .sidebar import SidebarView
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR


class ViewTabUI(Container):

    def __init__(self, controller: ViewTab, sidebar: SidebarView, **kwargs):
        super().__init__(**kwargs)

        self.style_ = {
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
            "align-self": "center",
            "padding": "0px 0px 0px 0px",
            "width": "100%",
            # "height": "480px",
            "margin": "0px 0px 0px 0px",
            # "border-radius": "8px",
            # "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller
        self.sidebar = sidebar
        self.mainbar = None

        self.build_mainbar()
        self.children = [self.sidebar, self.mainbar]

    def build_mainbar(self):
        title = CustomText("Experiment 2: Test", style_={"font-weight": "bold",
                                                         "font-size": "14px",
                                                         "margin": "0px 0px 8px 1px",
                                                         "align-self": "flex-start",
                                                         })
        map_ = Map(center=(4.2105, 101.9758), zoom=4)
        map_.layout.width = "618px"
        map_.layout.height = "570px"
        map_.layout.border = "1px solid " + PRIMARY_COLOR
        wrapper = Container(children=[title, map_],
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": "center",
                                "width": "618px",
                                "height": "600px",
                                "padding": "1px 1px 1px 1px",
                                "margin": "0px 0px 0px 24px",
                            })
        self.mainbar = wrapper
