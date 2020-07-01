from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Breadcrumbs(ReactWidget):

    _model_name = Unicode('BreadcrumbsModel').tag(sync=True)

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

    component = Unicode(None, allow_none=True).tag(sync=True)

    items_after_collapse = Float(None, allow_none=True).tag(sync=True)

    items_before_collapse = Float(None, allow_none=True).tag(sync=True)

    max_items = Float(None, allow_none=True).tag(sync=True)

    separator = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['Breadcrumbs']
