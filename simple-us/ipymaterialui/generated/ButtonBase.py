from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class ButtonBase(ReactWidget):

    _model_name = Unicode('ButtonBaseModel').tag(sync=True)

    action = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    button_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    center_ripple = Bool(None, allow_none=True).tag(sync=True)

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

    component = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    disable_ripple = Bool(None, allow_none=True).tag(sync=True)

    disable_touch_ripple = Bool(None, allow_none=True).tag(sync=True)

    focus_ripple = Bool(None, allow_none=True).tag(sync=True)

    focus_visible_class_name = Unicode(None, allow_none=True).tag(sync=True)

    role = Unicode(None, allow_none=True).tag(sync=True)

    tab_index = Union([
        Float(None, allow_none=True),
        Unicode(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    Touch_ripple_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    type = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['ButtonBase']
