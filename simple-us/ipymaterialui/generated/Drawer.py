from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Drawer(ReactWidget):

    _model_name = Unicode('DrawerModel').tag(sync=True)

    anchor = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    Backdrop_props = Dict(default_value=None, allow_none=True).tag(sync=True)

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

    elevation = Float(None, allow_none=True).tag(sync=True)

    Modal_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)

    Paper_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    Slide_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    theme = Dict(default_value=None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    variant = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['Drawer']
