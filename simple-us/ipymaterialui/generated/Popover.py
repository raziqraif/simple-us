from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Popover(ReactWidget):

    _model_name = Unicode('PopoverModel').tag(sync=True)

    anchor_el = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    anchor_origin = Dict(default_value=None, allow_none=True).tag(sync=True)

    anchor_position = Dict(default_value=None, allow_none=True).tag(sync=True)

    anchor_reference = Union([
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

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    container = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    elevation = Float(None, allow_none=True).tag(sync=True)

    margin_threshold = Float(None, allow_none=True).tag(sync=True)

    Modal_classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    Paper_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    transform_origin = Dict(default_value=None, allow_none=True).tag(sync=True)

    Transition_component = Unicode(None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True),
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)

    Transition_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    Backdrop_component = Unicode(None, allow_none=True).tag(sync=True)

    Backdrop_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    close_after_transition = Bool(None, allow_none=True).tag(sync=True)

    disable_auto_focus = Bool(None, allow_none=True).tag(sync=True)

    disable_backdrop_click = Bool(None, allow_none=True).tag(sync=True)

    disable_enforce_focus = Bool(None, allow_none=True).tag(sync=True)

    disable_escape_key_down = Bool(None, allow_none=True).tag(sync=True)

    disable_portal = Bool(None, allow_none=True).tag(sync=True)

    disable_restore_focus = Bool(None, allow_none=True).tag(sync=True)

    hide_backdrop = Bool(None, allow_none=True).tag(sync=True)

    keep_mounted = Bool(None, allow_none=True).tag(sync=True)

    manager = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['Popover']
