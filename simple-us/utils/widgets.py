from typing import Dict

from ipymaterialui import Html


class CustomText(Html):
    """ Custom text class to make sure the default text size is consistent.

    The default text size on Jupyter Lab and Jupyter Notebook is not consistent.
    """

    def __init__(self, text, tag="span", font_size=16, style_: Dict = None, **kwargs):
        super(Html, self).__init__()

        if style_ is None:
            style_ = {}

        style_["font-size"] = font_size

        self.tag = tag
        self.children = text
        self.style_ = style_
