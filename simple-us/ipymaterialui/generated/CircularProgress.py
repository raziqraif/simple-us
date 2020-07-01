from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class CircularProgress(ReactWidget):

    _model_name = Unicode('CircularProgressModel').tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    color = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    disable_shrink = Bool(None, allow_none=True).tag(sync=True)

    size = Union([
        Float(None, allow_none=True),
        Unicode(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)

    thickness = Float(None, allow_none=True).tag(sync=True)

    value = Float(None, allow_none=True).tag(sync=True)

    variant = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['CircularProgress']
