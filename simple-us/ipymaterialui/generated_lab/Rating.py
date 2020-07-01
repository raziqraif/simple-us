from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ..generated.ReactWidget import ReactWidget

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Rating(ReactWidget):

    _model_name = Unicode('RatingModel').tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    empty_icon = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

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

    Icon_container_component = Unicode(None, allow_none=True).tag(sync=True)

    max = Float(None, allow_none=True).tag(sync=True)

    name = Unicode(None, allow_none=True).tag(sync=True)

    precision = Float(None, allow_none=True).tag(sync=True)

    read_only = Bool(None, allow_none=True).tag(sync=True)

    size = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    value = Float(None, allow_none=True).tag(sync=True)


__all__ = ['Rating']
