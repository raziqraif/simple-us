from copy import copy
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
from ipywidgets import Accordion, Layout
from ipywidgets import Output

from model import Experiment
from utils.misc import DANGER_COLOR
from .controller import Details
from utils import BACKGROUND_COLOR
from utils import CustomText
from utils import CustomCheckbox
from utils import INNER_BACKGROUND_COLOR
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR


class DetailsView(Dialog):
    def __init__(self, controller: Details, experiment: Optional[Experiment]):
        super().__init__()
        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "flex-start",
            "align-items": "center",
            "align-self": "flex-start",

        }
        self.controller = controller
        self.open_ = False
        self.max_width = "lg"
        self.disable_backdrop_click = False
        self.on_event("onClick", self.controller.onclick_backdrop)

        self.experiment = experiment
        self._main = None
        self._title_bar: Optional[Container] = None
        accordion_layout = Layout(width="535px", margin="0px 0px 0px 4px", align_self="center")
        output_layout = Layout(width="535px", margin="0px 0px 0px 0px", align_self="center")
        self._log_output_area = Output(layout=accordion_layout)
        self._log_accordion = Accordion(children=[self._log_output_area], selected_index=None, layout=output_layout)
        self._log_accordion.set_title(0, "Log")

        self._buttons_wrapper: Optional[Container] = None
        self._download: Optional[Button] = None
        self._delete: Optional[Button] = None

        self._build_main()
        self.children = self._main  # Cannot be a list

    def _build_main(self):
        self._main = Paper(
            style_={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                # "width": "750px",  # max it can go
                "width": "650px",
                # "height": "750px",  # max it can go
                "height": "600px",
                "background": "white",
            })
        self._main.on_event("onClick", self.controller.onclick_backdrop)
        self._title_bar = self._create_title_bar()
        body = self._create_details_area()
        self._build_buttons_wrapper()
        self._main.children = [self._title_bar, body, self._buttons_wrapper]

    def _build_buttons_wrapper(self):
        self._download = self._create_button("Download", "cloud_download_outlined")
        self._delete = self._create_button("Delete", "delete", DANGER_COLOR)
        self._download.on_event("onClick", self.controller.onclick_download)
        self._delete.on_event("onClick", self.controller.onclick_delete)
        self._buttons_wrapper = Container(children=[self._download, self._delete],
                            style_={
                                "width": "100%",
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                                "align-items": "center",
                                "margin": "16px 0px 16px 0px",
                            })

    def _create_button(self, text: str, icon: str, background=PRIMARY_COLOR) -> Button:
        icon = Icon(children=icon, style_={"color": "white", "margin": "0px 0px 0px 8px"})
        button = Button(children=[CustomText(text,
                                             style_={
                                                 "display": "flex",
                                                 "align-items": "center",
                                                 "font-size": "11px",
                                                 "color": "#ffffff",
                                                 "align-self": "center",
                                             }), icon],
                        color="#454851",
                        focus_ripple=True,
                        style_={
                            "display": "flex",
                            "width": "140px",
                            "height": "32px",
                            "padding": "0px 0px 0px 0px",
                            "margin": "0px 4px 0px 8px",
                            "background": background,
                            "align-items": "center !important",
                        }, )
        return button

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

    def _create_details_area(self):
        bar = Container(style_={
            "display": "flex",
            "flex-direction": "column",
            "padding": "16px 48px 16px 48px",
            "align-items": "center",
            "justify-content": "flex-start",
            "background": "white",
            "width": "100%",
            "flex-grow": "1",
            "overflow-y": "scroll",
            "overflow-wrap": "break-word",
        })

        id_ = self._create_data_row("ID", self.experiment.id_str if self.experiment else "")
        name = self._create_data_row("Name", self.experiment.name_str if self.experiment else "")
        model = self._create_data_row("Model", self.experiment.model_str if self.experiment else "")
        status = self._create_data_row("Status", self.experiment.status_str if self.experiment else "")
        description = self._create_data_row("Description", self.experiment.description_str if self.experiment else "")
        author = self._create_data_row("Author", self.experiment.author_str if self.experiment else "")
        submission_id = self._create_data_row("Submission ID",
                                              self.experiment.submission_id_str if self.experiment else "")
        submission_time = self._create_data_row("Submission Time",
                                                self.experiment.submission_time_str if self.experiment else "")
        published = self._create_data_row("Published", self.experiment.published_str if self.experiment else "")
        published_style = copy(published.style_)
        published_style["margin"] = "8px 0px 16px 0px"
        published.style_ = published_style
        bar.children = [id_,
                        name,
                        model,
                        description,
                        author,
                        submission_id,
                        submission_time,
                        status,
                        published,
                        self._log_accordion]
        return bar

    def close(self):
        self.open_ = False

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
                                "wrap-word": "break-word",
                                "overflow-wrap": "break-word",
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
                                "width": "123px",
                                "minWidth": "123px",
                            })
        return wrapper

    def _create_data_value_wrapper(self, value: str):
        value_html = CustomText(value,
                                style_={
                                    "color": "black",
                                    "wrap": "hard",
                                    "max-width": "404px",
                                    "word-wrap": "break-word",
                                    "overflow-wrap": "break-word",
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
                                "wrap": "hard",
                                "word-wrap": "break-word",
                                "overflow-wrap": "break-word",
                            })
        return wrapper

    def show(self, experiment: Experiment):
        self.experiment = experiment
        details_area = self._create_details_area()

        print(experiment.id_str, experiment.is_private)
        # if experiment.is_private:
        #     self._buttons_wrapper.chilren = [self._download, self._delete]
        # else:
        #     self._buttons_wrapper.children = [self._download]
        self._log_output_area.clear_output()
        self._main.children = [self._title_bar, details_area, self._buttons_wrapper]
        self.open_ = True
