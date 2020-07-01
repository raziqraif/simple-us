from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Grow(ReactWidget):

    _model_name = Unicode('GrowModel').tag(sync=True)

    children = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    in_ = Bool(None, allow_none=True).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)

    timeout = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True),
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)


__all__ = ['Grow']
