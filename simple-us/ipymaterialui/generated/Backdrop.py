from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Backdrop(ReactWidget):

    _model_name = Unicode('BackdropModel').tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    invisible = Bool(None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)


__all__ = ['Backdrop']
