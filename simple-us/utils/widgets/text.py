from typing import Dict

from ipymaterialui import Html


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
