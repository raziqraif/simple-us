from typing import Dict

from ipymaterialui import IconButton, Icon


class CustomCheckbox(IconButton):
    """ Custom checkbox widget as the default mui.Checkbox seems to be unstable.

    User would need to manipulate the "checked" or "unchecked" manually by switching the value of
    the checked attribute.
    """

    def __init__(self, style_: Dict = None, **kwargs):
        super(IconButton, self).__init__()

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
            style_ = {
                "padding": "0px 0px 0px 0px",
                "width": "35px",
                "height": "35px",
            }

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
