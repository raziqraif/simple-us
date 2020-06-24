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

from .controller import CreateTab
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR


class CreateTabView(Container):

    def __init__(self, controller: CreateTab, **kwargs):
        super().__init__(**kwargs)

        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "align-self": "center",
            "padding": "32px 72px 40px 72px",
            "width": "550px",
            "height": "460px",
            "margin": "0px 0px 60px 0px",
            "border-radius": "8px",
            "background": INNER_BACKGROUND_COLOR,
        }

        self.controller = controller
        self.title = CustomText("New Experiment",
                                style_={
                                    ""
                                    "font-weight": "bold",
                                    "font-size": "18px",
                                    "margin": "0px 0px 0px 0px",
                                    "color": "black",
                                    # "text-decoration": "underline",
                                })
        self.model_wrapper = None
        self.name_wrapper = None
        self.description_wrapper = None
        self.configuration_wrapper = None
        self.submit = self._create_button("Submit")

        self._build_model_wrapper()
        self._build_name_wrapper()
        self._build_description_wrapper()
        self._build_configuration_wrapper()

        self.center_wrapper = Container(children=[self.title, self.model_wrapper, self.name_wrapper, ])

        self.children = [
            self.title,
            self.model_wrapper,
            self.name_wrapper,
            self.description_wrapper,
            self.configuration_wrapper,
            self.submit
        ]

    def _build_model_wrapper(self):
        label = self._create_label_wrapper("Model")
        self.model_wrapper = self._create_input_row_wrapper()
        custom_allcrops = self._create_menu_item("Custom AllCrops")
        custom_cornsoy = self._create_menu_item("Custom Cornsoy")
        # select = Select(children=[custom_allcrops, custom_cornsoy],
        #                 value="", autofocus=True, required=True,
        #                 # variant="outlined",
        #                 margin="dense",
        #                 style_={
        #                     "font-size": "12px",
        #                     "width": "150px",
        #                 })
        layout = Layout(width="250px")
        select = widgets.Dropdown(value="", options=["", "Custom AllCrop", "Custom Cornsoy"], layout=layout)

        self.model_wrapper.children = [label, select]

    def _build_name_wrapper(self):
        label = self._create_label_wrapper("Name")
        self.name_wrapper = self._create_input_row_wrapper()
        # field = TextField(autofocus=True, required=True,
        #                   # variant="outlined",
        #                   style_={
        #                       "height": "1px",
        #                       "font-size": "12px",
        #                       "width": "180px",
        #                       "padding": "0px 0px 0px 0px",
        #                   })
        layout = Layout(width="250px")
        field = widgets.Text(layout=layout)
        self.name_wrapper.children = [label, field]

    def _build_description_wrapper(self):
        label = self._create_label_wrapper("Description")
        self.description_wrapper = self._create_input_row_wrapper()
        # layout = Layout(width="250px", max_height="100px", overlow="scroll", display="flex")
        # text_area = widgets.Textarea(layout=layout, rows=3, placeholder="Optional")
        text_area = TextareaAutosize(
                                     style_={
                                         "padding": "4px 8px 4px 8px",
                                         "width": "250px",
                                         "height": "55px",
                                         "resize": "none",
                                         "font-size": "13px",
                                         "font-family": '''-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
                                         Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", 
                                         "Segoe UI Symbol"''',
                                         "border": "1px solid darkgrey"
                                     })
        self.description_wrapper.children = [label, text_area]

    def _build_configuration_wrapper(self):
        label = self._create_label_wrapper("Configuration File")
        self.configuration_wrapper = self._create_input_row_wrapper()
        input_ = Input(  # TODO: Figure out how to override the css properly.
            input_props={
                "type": "file",
                "border": "none",
            },
            style_={
                "font-size": "13px",
                "width": "250px",
                "border": "none",
            }
        )
        # layout = Layout(padding="0px 0px 0px 0px")
        # input_ = FileUpload(accept="", multiple=False, layout=layout)  # This is nice looking, but there's bug with
        # the counter value. A fix was supposedly already made in the official repository, but it is probably
        # not released yet.
        # https://github.com/jupyter-widgets/ipywidgets/pull/2666

        self.configuration_wrapper.children = [label, input_]

    def _create_input_row_wrapper(self):
        wrapper = Container(children=[],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "24px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                                "align-items": "center",
                                "justify-content": "flex-start",
                                "height": "auto",
                            })
        return wrapper

    def _create_label_wrapper(self, text: str):
        label = CustomText(text,
                           style_={
                               "color": "black",
                               "font-weight": "bold",
                           })
        wrapper = Container(children=[label],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "0px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                                "justify-content": "flex-start",
                                "align-items": "center",
                                "height": "auto",
                                "width": "150px",
                            })
        return wrapper

    def _create_menu_item(self, text) -> MenuItem:
        text_html = CustomText(text, style_={
            "font-size": "14px",
        })
        menu = MenuItem(children=[text_html],
                        value=text,
                        dense=True,
                        selected=False, style_={"background": "white"})
        return menu

    def _create_button(self, text, margin: str = "32px 0px 0px 0px") -> Button:
        button = Button(children=[CustomText(text,
                                             style_={
                                                 "display": "flex",
                                                 "align-items": "center",
                                                 "font-size": "12px",
                                                 "color": "#ffffff",
                                                 "align-self": "center",
                                             })],
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "display": "flex",
                            "width": "120px",
                            "height": "30px",
                            "padding": "0px 0px 0px 0px",
                            "margin": margin,
                            "background": PRIMARY_COLOR,
                            "align-items": "center !important",
                        }, )
        return button
