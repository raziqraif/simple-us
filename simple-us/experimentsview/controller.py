from typing import List
from typing import Optional

from .viewcontext import ViewContext
from map.layerservice import RasterLayerUtil
from map.layerservice import VectorLayerUtil
from .sidebar import Sidebar
from model import Experiment
from model.variableutil import VariableModel


class ViewTab:
    def __init__(self):
        from .view import ViewTabUI
        self._sidebar = Sidebar()
        self._sidebar.visualize_variables_callback = self.visualize_variables
        self.contexts: List[ViewContext] = []
        self.active_context: Optional[ViewContext] = None  # Needed to save the state of the previous context when
        # context switch happens

        self.view = ViewTabUI(self, self._sidebar.view)
        self._sidebar.close_tab_callback = self.view.close_tab

    def assign_maps(self, maps: List[any], context: ViewContext):
        assert isinstance(context, ViewContext)
        context.maps = maps

    def new_view(self, experiments: List[Experiment]) -> bool:
        """ New display/compare view"""

        context = ViewContext(experiments)
        if not context.variable_service.has_valid_variables():
            return False
        self.contexts.append(context)
        self.view.new_tab(context.title, context, context.is_comparison)
        return True

    def visualize_variables(self, system_component: str, spatial_resolution: str, type_of_result: str,
                            result_to_view: str, filter_min: int, filter_max: int) -> None:

        assert self.active_context is not None
        experiments = self.active_context.experiments
        maps = self.view.maps()
        count = len(experiments)
        assert count > 0
        assert len(maps) == len(experiments)

        for i in range(0, len(experiments)):
            variable_model = VariableModel(experiments[i].id_str, system_component, spatial_resolution, type_of_result,
                                           result_to_view, filter_min, filter_max)
            if variable_model.is_raster():
                layer_util = RasterLayerUtil(variable_model, self.active_context.session_id)
                layer = layer_util.create_layer()
                maps[i].visualize_raster(layer, layer_util.processed_raster_path)
            elif variable_model.is_vector():
                layer_util = VectorLayerUtil(variable_model, self.active_context.session_id)
                layer = layer_util.create_layer()
                maps[i].visualize_vector(layer)

    def onchange_tab(self, data):
        tab_index = data["new"]
        assert isinstance(tab_index, int)
        if tab_index >= 0:
            context = self.view.context(tab_index)
            self.switch_context(context)

    def switch_context(self, context: Optional[ViewContext]):
        if self.active_context:
            self.active_context.maps = self.view.maps()
        self.active_context = context
        self._sidebar.switch_context(context)

        if context is not None:
            self.view.show_maps(context)

    def onclick_close(self):
        pass
