from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Avatar(ReactWidget):

    _model_name = Unicode('AvatarModel').tag(sync=True)

    alt = Unicode(None, allow_none=True).tag(sync=True)

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

    children_class_name = Unicode(None, allow_none=True).tag(sync=True)

    classes = Dict(default_value=None, allow_none=True).tag(sync=True)

    class_name = Unicode(None, allow_none=True).tag(sync=True)

    component = Unicode(None, allow_none=True).tag(sync=True)

    img_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    sizes = Unicode(None, allow_none=True).tag(sync=True)

    src = Unicode(None, allow_none=True).tag(sync=True)

    src_set = Unicode(None, allow_none=True).tag(sync=True)


__all__ = ['Avatar']
