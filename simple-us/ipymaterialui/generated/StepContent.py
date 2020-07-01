from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class StepContent(ReactWidget):

    _model_name = Unicode('StepContentModel').tag(sync=True)

    active = Bool(None, allow_none=True).tag(sync=True)

    alternative_label = Bool(None, allow_none=True).tag(sync=True)

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

    completed = Bool(None, allow_none=True).tag(sync=True)

    last = Bool(None, allow_none=True).tag(sync=True)

    optional = Bool(None, allow_none=True).tag(sync=True)

    orientation = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)

    Transition_component = Unicode(None, allow_none=True).tag(sync=True)

    transition_duration = Union([
        Float(None, allow_none=True),
        Dict(default_value=None, allow_none=True),
        Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True, **widget_serialization)

    Transition_props = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['StepContent']
