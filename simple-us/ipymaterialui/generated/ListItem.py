from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class ListItem(ReactWidget):

    _model_name = Unicode('ListItemModel').tag(sync=True)

    align_items = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    auto_focus = Bool(None, allow_none=True).tag(sync=True)

    button = Bool(None, allow_none=True).tag(sync=True)

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

    Container_component = Unicode(None, allow_none=True).tag(sync=True)

    Container_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    dense = Bool(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    disable_gutters = Bool(None, allow_none=True).tag(sync=True)

    divider = Bool(None, allow_none=True).tag(sync=True)

    focus_visible_class_name = Unicode(None, allow_none=True).tag(sync=True)

    selected = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['ListItem']
