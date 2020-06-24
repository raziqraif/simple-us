from copy import copy

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
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "align-self": "center",
            "padding": "0px 0px 0px 0px",
            # "width": "550px",
            # "height": "480px",
            "margin": "0px 0px 0px 0px",
            # "border-radius": "8px",
            # "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller
        self.children = [sidebar]
