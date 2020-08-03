from typing import Any
from typing import List
from typing import Optional

from ipymaterialui import Button
from ipymaterialui import Container
from ipymaterialui import Html
from ipymaterialui import Icon
from ipymaterialui import IconButton
from ipymaterialui import Dialog
from ipymaterialui import DialogContent
from ipymaterialui import DialogTitle
from ipymaterialui import Modal
from ipymaterialui import Paper

from model import Experiment
from .controller import Details
from utils import BACKGROUND_COLOR
from utils import CustomText
from utils import CustomCheckbox
from utils import INNER_BACKGROUND_COLOR
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR


class DetailsView(Dialog):
    def __init__(self, controller: Details, experiment: Experiment):
        super().__init__()
        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "flex-start",
            "align-items": "center",
            "align-self": "flex-start",

        }
        self.controller = controller
        self.open_ = True
        self.max_width = "lg"
        self.disable_backdrop_click = False
        self.on_event("onClick", self.controller.onclick_backdrop)
        self._main = None
        self._experiment = experiment

        self._build_main()
        self.children = self._main  # Cannot be a list

    def _build_main(self):
        self._main = Paper(
            style_={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                # "width": "750px",
                "width": "650px",
                "height": "750px",
                "background": "white",
                # "overflow-y": "scroll",
            })
        self._main.on_event("onClick", self.controller.onclick_backdrop)
        title_bar = self._create_title_bar()
        body = self._create_body()
        self._main.children = [title_bar, body]

    def _create_title_bar(self):
        bar = Container(style_={
            "display": "flex",
            "flex-direction": "row",
            "align-items": "center",
            "justify-content": "flex-start",
            "background": PRIMARY_COLOR,
            "padding": "16px 16px 16px 32px",
            "width": "100%",
            "flex-grow": "0",
        })
        title = DialogTitle(children=["Experiment Details"],
                            style_={"color": "white",
                                    "flex-grow": "1",
                                    "padding": "0px 0px 0px 0px",
                                    "font-size": "16px",
                                    })
        close_icon = Icon(children="close",
                          style_={
                              "color": "white",
                              "font-size": "21px",
                              "padding": "0px 0px 0px 0px",
                          })
        close_button = IconButton(children=close_icon,
                                  style_={
                                      "width": "35px",
                                      "height": "35px",
                                      "padding": "0px 0px 0px 0px",
                                  })
        close_button.on_event("onClick", self.controller.onclose)
        bar.children = [title, close_button]
        return bar

    def _create_body(self):
        bar = Container(style_={
            "display": "flex",
            "flex-direction": "column",
            "padding": "16px 48px 16px 48px",
            "align-items": "center",
            "justify-content": "flex-start",
            "background": "white",
            "width": "100%",
            "flex-grow": "1",
            "overflow-y": "scroll"
        })

        id_ = self._create_data_row("ID", self._experiment.id_str)
        name = self._create_data_row("Name", self._experiment.name_str)
        model = self._create_data_row("Model", self._experiment.model_str)
        status = self._create_data_row("Status", self._experiment.status_str)
        description = self._create_data_row("Description", self._experiment.description_str)
        author = self._create_data_row("Author", self._experiment.author_str)
        submission_id = self._create_data_row("Submission ID", self._experiment.submission_id_str)
        submission_time = self._create_data_row("Submission Time", self._experiment.submission_time_str)
        published = self._create_data_row("Published", self._experiment.published_str)
        bar.children = [id_,
                        name,
                        model,
                        description,
                        author,
                        submission_id,
                        submission_time,
                        status,
                        published]
        return bar

    def close(self):
        print("closing")
        self.open_ = False
        del self  # It seems like the application becomes slow if the object does not get explicitly deleted

    def _create_data_row(self, label: str, value: str):
        wrapper = Container(children=[],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "8px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                                "align-items": "flex-start",
                                "justify-content": "flex-start",
                                "height": "auto",
                            })
        label_wrapper = self._create_data_label_wrapper(label)
        value_wrapper = self._create_data_value_wrapper(value)
        wrapper.children = [label_wrapper, ":", value_wrapper]
        return wrapper

    def _create_data_label_wrapper(self, text: str):
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
                                "align-items": "flex-start",
                                "height": "auto",
                                "width": "150px",
                            })
        return wrapper

    def _create_data_value_wrapper(self, value: str):
        value_html = CustomText(value,
                                style_={
                                    "color": "black",
                                })
        wrapper = Container(children=[value_html],
                            style_={
                                "display": "flex",
                                "flex-direction": "row",
                                "margin": "0px 0px 0px 8px",
                                "padding": "0px 0px 0px 0px",
                                "justify-content": "flex-start",
                                "align-items": "center",
                                "height": "auto",
                                "flex-grow": "1",
                            })
        return wrapper
