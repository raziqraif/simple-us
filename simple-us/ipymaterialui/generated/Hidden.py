from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Hidden(ReactWidget):

    _model_name = Unicode('HiddenModel').tag(sync=True)

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

    implementation = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    initial_width = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    lg_down = Bool(None, allow_none=True).tag(sync=True)

    lg_up = Bool(None, allow_none=True).tag(sync=True)

    md_down = Bool(None, allow_none=True).tag(sync=True)

    md_up = Bool(None, allow_none=True).tag(sync=True)

    only = Union([
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True),
        List(Any(), default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)

    sm_down = Bool(None, allow_none=True).tag(sync=True)

    sm_up = Bool(None, allow_none=True).tag(sync=True)

    xl_down = Bool(None, allow_none=True).tag(sync=True)

    xl_up = Bool(None, allow_none=True).tag(sync=True)

    xs_down = Bool(None, allow_none=True).tag(sync=True)

    xs_up = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['Hidden']
