from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class StepConnector(ReactWidget):

    _model_name = Unicode('StepConnectorModel').tag(sync=True)

    active = Bool(None, allow_none=True).tag(sync=True)

    alternative_label = Bool(None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    completed = Bool(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    index = Float(None, allow_none=True).tag(sync=True)

    orientation = Union([
        Any(),
        Instance(DOMWidget),
        List(Instance(DOMWidget))
    ], default_value=None, allow_none=True).tag(sync=True, **widget_serialization)


__all__ = ['StepConnector']
