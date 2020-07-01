from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class MenuList(ReactWidget):

    _model_name = Unicode('MenuListModel').tag(sync=True)

    actions = Dict(default_value=None, allow_none=True).tag(sync=True)

    auto_focus = Bool(None, allow_none=True).tag(sync=True)

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

    disable_list_wrap = Bool(None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    dense = Bool(None, allow_none=True).tag(sync=True)

    disable_padding = Bool(None, allow_none=True).tag(sync=True)

    subheader = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['MenuList']
