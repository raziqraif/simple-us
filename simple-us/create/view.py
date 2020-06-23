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
            "padding": "48px 48px 48px 48px",
            "width": "500px",
            "height": "550px",
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
                                    "margin": "0px 0px 16px 0px",
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
        select = Select(children=[custom_allcrops, custom_cornsoy],
                        value="", autofocus=True, required=True,
                        # variant="outlined",
                        margin="dense",
                        style_={
                            "font-size": "12px",
                            "width": "150px",
                        })

        self.model_wrapper.children = [label, select]

    def _build_name_wrapper(self):
        label = self._create_label_wrapper("Name")
        self.name_wrapper = self._create_input_row_wrapper()
        field = TextField(autofocus=True, required=True,
                          # variant="outlined",
                          style_={
                              "height": "1px",
                              "font-size": "12px",
                              "width": "180px",
                          })
        self.name_wrapper.children = [label, field]

    def _build_description_wrapper(self):
        label = self._create_label_wrapper("Description")
        self.description_wrapper = self._create_input_row_wrapper()
        text_area = TextField(autofocus=True,
                              # variant="outlined",
                              value="",
                              # multiline=True,
                              input_props={"style_": {"font-size": "4px"}},
                              style_={
                                  "font-size": "4px",
                                  "width": "250px",
                                  "height": "180px",
                                  "maxHeight": "150px",
                              })
        self.description_wrapper.children = [label, text_area]

    def _build_configuration_wrapper(self):
        label = self._create_label_wrapper("Configuration File")
        self.configuration_wrapper = self._create_input_row_wrapper()
        upload = self._create_button("Upload", "0px 0px 0px 0px")
        upload.children = [Input(type="file",
                                 style_={"display": "none"})]
        self.configuration_wrapper.children = [label, upload]

    def _create_input_row_wrapper(self):
        wrapper = Container(children=[],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "24px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
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
        button = Button(children=CustomText(text,
                                            style_={
                                                "display": "flex",
                                                "align-items": "center",
                                                "font-size": "12px",
                                                "color": "#ffffff",
                                                "align-self": "center",
                                            }),
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "display": "flex",

                            "width": "120px",
                            "height": "30px",
                            "padding": "0px 0px 0px 0px",
                            "margin": margin,
                            "background": PRIMARY_COLOR,
                        }, )
        return button
