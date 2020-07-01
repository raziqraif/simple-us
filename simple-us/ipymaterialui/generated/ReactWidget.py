from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization
from ..Events import Events


class ReactWidget(DOMWidget, Events):

    _model_name = Unicode('ReactWidgetModel').tag(sync=True)

    _view_name = Unicode('ReactView').tag(sync=True)

    _view_module = Unicode('jupyter-materialui').tag(sync=True)

    _model_module = Unicode('jupyter-materialui').tag(sync=True)

    _view_module_version = Unicode('^0.1.4').tag(sync=True)

    _model_module_version = Unicode('^0.1.4').tag(sync=True)

    _metadata = Dict(default_value=None, allow_none=True).tag(sync=True)

    _events = List(Unicode(), default_value=None, allow_none=True).tag(sync=True)

    style_ = Dict(default_value=None, allow_none=True).tag(sync=True)


__all__ = ['ReactWidget']
