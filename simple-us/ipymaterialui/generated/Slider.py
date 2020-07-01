from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Slider(ReactWidget):

    _model_name = Unicode('SliderModel').tag(sync=True)

    aria_label = Unicode(None, allow_none=True).tag(sync=True)

    aria_labelledby = Unicode(None, allow_none=True).tag(sync=True)

    aria_valuetext = Unicode(None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    default_value = Union([
        Float(None, allow_none=True),
        List(Float(), default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    marks = Union([
        Bool(None, allow_none=True),
        List(Any(), default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    max = Float(None, allow_none=True).tag(sync=True)

    min = Float(None, allow_none=True).tag(sync=True)

    name = Unicode(None, allow_none=True).tag(sync=True)

    orientation = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    step = Float(None, allow_none=True).tag(sync=True)

    Thumb_component = Unicode(None, allow_none=True).tag(sync=True)

    value = Union([
        Float(None, allow_none=True),
        List(Float(), default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    Value_label_component = Unicode(None, allow_none=True).tag(sync=True)

    value_label_display = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    value_label_format = Union([
        Unicode(None, allow_none=True)
    ], default_value=None).tag(sync=True)


__all__ = ['Slider']
