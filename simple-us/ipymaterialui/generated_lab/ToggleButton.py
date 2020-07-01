from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ..generated.ReactWidget import ReactWidget

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class ToggleButton(ReactWidget):

    _model_name = Unicode('ToggleButtonModel').tag(sync=True)

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

    disabled = Bool(None, allow_none=True).tag(sync=True)

    disable_focus_ripple = Bool(None, allow_none=True).tag(sync=True)

    disable_ripple = Bool(None, allow_none=True).tag(sync=True)

    selected = Bool(None, allow_none=True).tag(sync=True)

    size = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['ToggleButton']
