from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ..generated.ReactWidget import ReactWidget

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class SpeedDialIcon(ReactWidget):

    _model_name = Unicode('SpeedDialIconModel').tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    icon = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    open_icon = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['SpeedDialIcon']
