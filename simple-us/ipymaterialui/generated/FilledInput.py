from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class FilledInput(ReactWidget):

    _model_name = Unicode('FilledInputModel').tag(sync=True)

    auto_complete = Unicode(None, allow_none=True).tag(sync=True)

    auto_focus = Bool(None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    default_value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    disable_underline = Bool(None, allow_none=True).tag(sync=True)

    end_adornment = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    error = Bool(None, allow_none=True).tag(sync=True)

    full_width = Bool(None, allow_none=True).tag(sync=True)

    id = Unicode(None, allow_none=True).tag(sync=True)

    input_component = Unicode(None, allow_none=True).tag(sync=True)

    input_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    input_ref = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    margin = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    multiline = Bool(None, allow_none=True).tag(sync=True)

    name = Unicode(None, allow_none=True).tag(sync=True)

    placeholder = Unicode(None, allow_none=True).tag(sync=True)

    read_only = Bool(None, allow_none=True).tag(sync=True)

    required = Bool(None, allow_none=True).tag(sync=True)

    rows = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    rows_max = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    start_adornment = Union([
        Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None),
        List(Union([
        Unicode(),
        Instance(DOMWidget)
    ], default_value=None))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    type = Unicode(None, allow_none=True).tag(sync=True)

    value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    aria_describedby = Unicode(None, allow_none=True).tag(sync=True)

    select = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['FilledInput']
