from ipymaterialui import Container, Button
from ipymaterialui import Html

from .controller import CreateTab
from utils import CustomText
from utils import PRIMARY_COLOR


class CreateTabView(Container):

    def __init__(self, controller: CreateTab, **kwargs):
        super().__init__(**kwargs)

        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
        }

        self.controller = controller
        self.title = CustomText("New Experiment",
                                style_={
                                    "font-weight": "bold",
                                    "font-size": "20px",
                                    "text-decoration": "underline",
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
        self.model_wrapper.children = [label]

    def _build_name_wrapper(self):
        label = self._create_label_wrapper("Name")
        self.name_wrapper = self._create_input_row_wrapper()
        self.name_wrapper.children = [label]

    def _build_description_wrapper(self):
        label = self._create_label_wrapper("Description")
        self.description_wrapper = self._create_input_row_wrapper()
        self.description_wrapper.children = [label]

    def _build_configuration_wrapper(self):
        label = self._create_label_wrapper("Configuration File")
        self.configuration_wrapper = self._create_input_row_wrapper()
        self.configuration_wrapper.children = [label]

    def _create_input_row_wrapper(self):
        wrapper = Container(children=[],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "24px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                                "justify-content": "flex-start",
                                "height": "auto",
                                "width": "500px",
                            })
        return wrapper

    def _create_label_wrapper(self, text: str):
        label = CustomText(text,
                           style_={
                               "font-weight": "bold",
                           })
        wrapper = Container(children=[label],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "0px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                                "justify-content": "flex-start",
                                "height": "auto",
                                "width": "200px",
                            })
        return wrapper

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
                            "width": "135px",
                            "height": "34px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "0px 0px 0px 8px",
                            "background": PRIMARY_COLOR,
                        }, )
        return button
