from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ..generated.ReactWidget import ReactWidget

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class SpeedDial(ReactWidget):

    _model_name = Unicode('SpeedDialModel').tag(sync=True)

    ariaLabel = Unicode(None, allow_none=True).tag(sync=True)

    Button_props = Dict(default_value=None, allow_none=True).tag(sync=True)

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

    direction = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    hidden = Bool(None, allow_none=True).tag(sync=True)

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

    Transition_component = Unicode(None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    Transition_props = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['SpeedDial']
