from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Slide(ReactWidget):

    _model_name = Unicode('SlideModel').tag(sync=True)

    children = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    direction = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    in_ = Bool(None, allow_none=True).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)

    timeout = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)


__all__ = ['Slide']
