from copy import copy
from typing import Optional

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
# from ipywidgets import FileUpload
from ipywidgets import Layout

from .controller import CreateTab
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
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
            # "border-radius": "8px",
            "border": "1px solid " + PRIMARY_COLOR,
            # "background": INNER_BACKGROUND_COLOR,
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
        self._model_wrapper: Optional[Container] = None
        self._name_wrapper: Optional[Container] = None
        self._description_wrapper: Optional[Container] = None
        self._configuration_wrapper: Optional[Container] = None
        self._uploaded_file: Optional[CustomText] = None

        self._model_select: Optional[Select] = None
        self._name_textbox: Optional[widgets.Text] = None
        self._description_textbox: Optional[widgets.Textarea] = None
        self._submit: Button = self._create_button("Submit")
        self._submit.on_event("onClick", self.controller.onclick_submit)

        self._build_model_wrapper()
        self._build_name_wrapper()
        self._build_description_wrapper()
        self._build_configuration_wrapper()

        self.center_wrapper = Container(children=[self.title, self._model_wrapper, self._name_wrapper, ])

        self.children = [
            self.title,
            self._model_wrapper,
            self._name_wrapper,
            self._description_wrapper,
            self._configuration_wrapper,
            self._submit
        ]

    def _build_model_wrapper(self):
        label = self._create_label_wrapper("Model")
        self._model_wrapper = self._create_input_row_wrapper()
        layout = Layout(width="250px")
        self._model_select = widgets.Dropdown(value="", options=["", "Custom AllCrops", "Custom CornSoy"],
                                              layout=layout)

        self._model_wrapper.children = [label, self._model_select]

    def _build_name_wrapper(self):
        label = self._create_label_wrapper("Name")
        self._name_wrapper = self._create_input_row_wrapper()
        layout = Layout(width="250px")
        self._name_textbox = widgets.Text(layout=layout, value="")
        self._name_wrapper.children = [label, self._name_textbox]

    def _build_description_wrapper(self):
        label = self._create_label_wrapper("Description")
        self._description_wrapper = self._create_input_row_wrapper()
        self._description_textbox = TextareaAutosize(
            value="",
            style_={
                "margin": "0px 0px 0px 2px",
                "padding": "4px 8px 4px 8px",
                "width": "250px",
                "height": "55px",
                "resize": "none",
                "font-size": "13px",
                "font-family": '''"Roboto", "Helvetica", "Arial", sans-serif''',
                "border": "1px solid darkgrey"
            })
        self._description_wrapper.children = [label, self._description_textbox]

    def _build_configuration_wrapper(self):
        label = self._create_label_wrapper("Configuration File")
        self._configuration_wrapper = self._create_input_row_wrapper()
        layout = Layout(width="100px", padding="0px 0px 0px 0px", margin="0px 8px 0px 0px")
        upload_btn = widgets.Button(description="Upload", layout=layout)
        self._uploaded_file = CustomText('No file uploaded', style_={"align-self": "center",
                                                                     "font-size": "13px",
                                                                     "margin": "0px 0x 0px 0px",
                                                                     "padding": "0px 0x 0px 0px",
                                                                     "overflow": "hidden",
                                                                     "text-overflow": "ellipsis",
                                                                     "white-space": "nowrap",
                                                                     "width": "130px"
                                                                     })
        # https://github.com/jupyter-widgets/ipywidgets/pull/2666

        self._configuration_wrapper.children = [label, upload_btn, self._uploaded_file]

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
                            "height": "32px",
                            "padding": "0px 0px 0px 0px",
                            "margin": margin,
                            "background": PRIMARY_COLOR,
                            "align-items": "center !important",
                        }, )
        return button

    @property
    def model(self) -> str:
        return self._model_select.value.strip()

    @property
    def name(self) -> str:
        return self._name_textbox.value.strip()

    @property
    def description(self) -> str:
        return self._description_textbox.value.strip()

    def clear_form(self):
        self._model_select.value = ""
        self._name_textbox.value = ""
        self._description_textbox.value = ""
        self._uploaded_file.children = "No file uploaded"
