from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)

from .ReactWidget import ReactWidget
from ipywidgets import DOMWidget
from ipywidgets.widgets.widget import widget_serialization


class Modal(ReactWidget):

    _model_name = Unicode('ModalModel').tag(sync=True)

    Backdrop_component = Unicode(None, allow_none=True).tag(sync=True)

    Backdrop_props = Dict(default_value=None, allow_none=True).tag(sync=True)

    children = Instance(DOMWidget, allow_none=True).tag(sync=True, **widget_serialization)

    close_after_transition = Bool(None, allow_none=True).tag(sync=True)

    container = Union([
        Dict(default_value=None, allow_none=True)
    ], default_value=None).tag(sync=True)

    disable_auto_focus = Bool(None, allow_none=True).tag(sync=True)

    disable_backdrop_click = Bool(None, allow_none=True).tag(sync=True)

    disable_enforce_focus = Bool(None, allow_none=True).tag(sync=True)

    disable_escape_key_down = Bool(None, allow_none=True).tag(sync=True)

    disable_portal = Bool(None, allow_none=True).tag(sync=True)

    disable_restore_focus = Bool(None, allow_none=True).tag(sync=True)

    hide_backdrop = Bool(None, allow_none=True).tag(sync=True)

    keep_mounted = Bool(None, allow_none=True).tag(sync=True)

    manager = Dict(default_value=None, allow_none=True).tag(sync=True)

    open_ = Bool(None, allow_none=True).tag(sync=True)


__all__ = ['Modal']
