from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Portal(ReactWidget):

    _model_name = Unicode('PortalModel').tag(sync=True)

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

    container = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    disable_portal = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['Portal']
