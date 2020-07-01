from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Popper(ReactWidget):

    _model_name = Unicode('PopperModel').tag(sync=True)

    anchor_el = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    children = Union([
        Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)

    container = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    disable_portal = Bool(None, allow_none=True).tag(sync=True)

    keep_mounted = Bool(None, allow_none=True).tag(sync=True)

    modifiers = Dict(default_value=None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    placement = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    popper_options = Dict(default_value=None, allow_none=True).tag(sync=True)

    popper_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    transition = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['Popper']
