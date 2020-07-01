from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class GridList(ReactWidget):

    _model_name = Unicode('GridListModel').tag(sync=True)

    cell_height = Union([
        Float(None, allow_none=True),
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)

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

    cols = Float(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    spacing = Float(None, allow_none=True).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['GridList']
