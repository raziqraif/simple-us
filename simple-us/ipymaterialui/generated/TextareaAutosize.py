from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class TextareaAutosize(ReactWidget):

    _model_name = Unicode('TextareaAutosizeModel').tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    placeholder = Unicode(None, allow_none=True).tag(sync=True)

    rows = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    rows_max = Union([
        Unicode(None, allow_none=True),
        Float(None, allow_none=True)
    ], default_value=None).tag(sync=True)

    style = Dict(default_value=None, allow_none=True).tag(sync=True)

    value = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['TextareaAutosize']
