from typing import Dict, Optional

from ipymaterialui import Chip
from ipymaterialui import Icon

from .text import CustomText


class ExperimentChip(Chip):
    def __init__(self, experiment_id: str, experiment_name: str, text_width: str = "100px", variant: str = "outlined",
                 style_: Optional[Dict] = None):

        super(Chip, self).__init__()

        style_ = style_ if style_ is not None else {}
        self.label = CustomText(experiment_name,
                                style_={
                                    "font-size": "13px",
                                    "text-align": "center",
                                    "overflow": "hidden",
                                    "text-overflow": "ellipsis",
                                    "width": text_width,
                                })
        self.delete_icon = Icon(children="close",
                                style_={
                                    "font-size": "15px",
                                    "padding": "0px 0px 0px 0px",
                                })

        self.experiment_name = experiment_name
        self.experiment_id = experiment_id
        self.clickable = False
        self.variant = variant
        self.style_ = style_
