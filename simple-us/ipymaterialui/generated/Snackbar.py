from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Snackbar(ReactWidget):

    _model_name = Unicode('SnackbarModel').tag(sync=True)

    action = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    anchor_origin = Dict(default_value=None, allow_none=True).tag(sync=True)

    auto_hide_duration = Float(None, allow_none=True).tag(sync=True)

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

    Click_away_listener_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    Content_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    disable_window_blur_listener = Bool(None, allow_none=True).tag(sync=True)

    key = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    message = Union([
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

    resume_hide_duration = Float(None, allow_none=True).tag(sync=True)

    Transition_component = Unicode(None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    Transition_props = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['Snackbar']
