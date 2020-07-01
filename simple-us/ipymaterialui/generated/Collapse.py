from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Collapse(ReactWidget):

    _model_name = Unicode('CollapseModel').tag(sync=True)

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

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    collapsed_height = Unicode(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    in_ = Bool(None, allow_none=True).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)

    theme = Dict(default_value=None, allow_none=True).tag(sync=True)

    timeout = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True),
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)


__all__ = ['Collapse']
