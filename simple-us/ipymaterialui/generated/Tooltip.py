from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Tooltip(ReactWidget):

    _model_name = Unicode('TooltipModel').tag(sync=True)

    children = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    disable_focus_listener = Bool(None, allow_none=True).tag(sync=True)

    disable_hover_listener = Bool(None, allow_none=True).tag(sync=True)

    disable_touch_listener = Bool(None, allow_none=True).tag(sync=True)

    enter_delay = Float(None, allow_none=True).tag(sync=True)

    enter_touch_delay = Float(None, allow_none=True).tag(sync=True)

    id = Unicode(None, allow_none=True).tag(sync=True)

    interactive = Bool(None, allow_none=True).tag(sync=True)

    leave_delay = Float(None, allow_none=True).tag(sync=True)

    leave_touch_delay = Float(None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    placement = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    Popper_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    theme = Dict(default_value=None, allow_none=True).tag(sync=True)

    title = Union([
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

    Transition_props = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['Tooltip']
