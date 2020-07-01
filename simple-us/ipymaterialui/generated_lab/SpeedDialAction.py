from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ..generated.ReactWidget import ReactWidget

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class SpeedDialAction(ReactWidget):

    _model_name = Unicode('SpeedDialActionModel').tag(sync=True)

    Button_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    delay = Float(None, allow_none=True).tag(sync=True)

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

    id = Unicode(None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    Tooltip_classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    tooltip_open = Bool(None, allow_none=True).tag(sync=True)

    tooltip_placement = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    tooltip_title = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['SpeedDialAction']
