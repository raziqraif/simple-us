from typing import Dict

from ipymaterialui import Icon
from ipymaterialui import IconButton
from ipymaterialui import Html
from ipywidgets import jslink


class CustomText(Html):
    """ Custom text class to make sure the default text size is consistent.

    The default text size on Jupyter Lab and Jupyter Notebook is not consistent.
    """

    def __init__(self, text, tag="div", style_: Dict = None, **kwargs):
        super(Html, self).__init__()

        if style_ is None:
            style_ = {
            }
        if "padding" not in style_.keys():
            style_["padding"] = "0px 0px 0px 0px"
        if "font-size" not in style_.keys():
            style_["font-size"] = 15

        self.tag = tag
        self.children = text
        self.style_ = style_


class CustomCheckbox(IconButton):
    """ Custom checkbox widget as the default mui.Checkbox seems to be instable.

    User would need to manipulate the "checked" or "unchecked" manually by switching the value of
    the checked attribute.
    """

    def __init__(self, style_: Dict = None, **kwargs):
        super(IconButton, self).__init__(**kwargs)

        self._checked_icon = Icon(children="check_box",
                                  style_={
                                      "color": "#f50057",
                                      "font-size": "20px",
                                      "padding": "0px 0px 0px 0px"
                                  })
        self._unchecked_icon = Icon(children="check_box_outline_blank",
                                    style_={
                                        "font-size": "20px",
                                        "padding": "0px 0px 0px 0px"
                                    })

        self._checked = False

        if style_ is None:
            style_ = {"padding": "8px 8px 8px 8px"}

        self.style_ = style_
        self.children = self._unchecked_icon

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        self._checked = value

        if self._checked:
            self.children = self._checked_icon
        elif not self._checked:
            self.children = self._unchecked_icon


