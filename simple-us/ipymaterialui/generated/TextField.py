from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class TextField(ReactWidget):

    _model_name = Unicode('TextFieldModel').tag(sync=True)

    auto_complete = Unicode(None, allow_none=True).tag(sync=True)

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

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    default_value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    error = Bool(None, allow_none=True).tag(sync=True)

    Form_helper_text_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    full_width = Bool(None, allow_none=True).tag(sync=True)

    helper_text = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    id = Unicode(None, allow_none=True).tag(sync=True)

    Input_label_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    Input_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    input_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    input_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    label = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    margin = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    multiline = Bool(None, allow_none=True).tag(sync=True)

    name = Unicode(None, allow_none=True).tag(sync=True)

    placeholder = Unicode(None, allow_none=True).tag(sync=True)

    required = Bool(None, allow_none=True).tag(sync=True)

    rows = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    rows_max = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    select = Bool(None, allow_none=True).tag(sync=True)

    Select_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    type = Unicode(None, allow_none=True).tag(sync=True)

    value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    variant = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    component = Unicode(None, allow_none=True).tag(sync=True)


__all__ = ['TextField']
