from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class CardMedia(ReactWidget):

    _model_name = Unicode('CardMediaModel').tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    image = Unicode(None, allow_none=True).tag(sync=True)

    src = Unicode(None, allow_none=True).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['CardMedia']
