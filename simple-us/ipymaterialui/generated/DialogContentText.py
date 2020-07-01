from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class DialogContentText(ReactWidget):

    _model_name = Unicode('DialogContentTextModel').tag(sync=True)

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

    align = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    color = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    component = Unicode(None, allow_none=True).tag(sync=True)

    display = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    gutter_bottom = Bool(None, allow_none=True).tag(sync=True)

    no_wrap = Bool(None, allow_none=True).tag(sync=True)

    paragraph = Bool(None, allow_none=True).tag(sync=True)

    theme = Dict(default_value=None, allow_none=True).tag(sync=True)

    variant = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    variant_mapping = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['DialogContentText']
