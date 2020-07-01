from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class TablePagination(ReactWidget):

    _model_name = Unicode('TablePaginationModel').tag(sync=True)

    Actions_component = Unicode(None, allow_none=True).tag(sync=True)

    back_icon_button_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    col_span = Float(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    count = Float(None, allow_none=True).tag(sync=True)

    label_rows_per_page = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    next_icon_button_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    page = Float(None, allow_none=True).tag(sync=True)

    rows_per_page = Float(None, allow_none=True).tag(sync=True)

    rows_per_page_options = List(Any(), default_value=None, allow_none=True).tag(sync=True)

    Select_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    align = Union([
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

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    padding = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    scope = Unicode(None, allow_none=True).tag(sync=True)

    size = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    sort_direction = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    variant = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['TablePagination']
