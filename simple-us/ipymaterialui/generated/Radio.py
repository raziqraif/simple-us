from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Radio(ReactWidget):

    _model_name = Unicode('RadioModel').tag(sync=True)

    checked = Bool(None, allow_none=True).tag(sync=True)

    checked_icon = Union([
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

    color = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    disable_ripple = Bool(None, allow_none=True).tag(sync=True)

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

    input_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    input_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    name = Unicode(None, allow_none=True).tag(sync=True)

    type = Unicode(None, allow_none=True).tag(sync=True)

    value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

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

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    disable_focus_ripple = Bool(None, allow_none=True).tag(sync=True)

    edge = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    size = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    action = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    button_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    center_ripple = Bool(None, allow_none=True).tag(sync=True)

    component = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    disable_touch_ripple = Bool(None, allow_none=True).tag(sync=True)

    focus_ripple = Bool(None, allow_none=True).tag(sync=True)

    focus_visible_class_name = Unicode(None, allow_none=True).tag(sync=True)

    role = Unicode(None, allow_none=True).tag(sync=True)

    tab_index = Union([
        Float(None, allow_none=True),
        Unicode(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    Touch_ripple_props = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['Radio']
