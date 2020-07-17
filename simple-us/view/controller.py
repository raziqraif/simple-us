from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

from .context import ViewContext
from .map import MapService
from .sidebar import Sidebar
from model import Experiment


class ViewTab:
    def __init__(self):
        from .view import ViewTabUI
        self._sidebar = Sidebar()
        self._sidebar.visualize_variables = self.visualize_variables
        self.contexts: List[ViewContext] = []
        self.active_context: Optional[ViewContext] = None  # Needed to save the state of the previous context when
        # context switch happens

        self.view = ViewTabUI(self, self._sidebar.view)

    def cache_maps(self, maps: List[any], context: ViewContext):
        assert isinstance(context, ViewContext)
        context.maps = maps

    def new_view(self, experiments: List[Experiment]):
        """ New display/compare view"""

        context = ViewContext(experiments)
        self.contexts.append(context)
        self.view.new_tab(context.title, context, context.is_comparison)
        # self._switch_context(context)

    def _switch_context(self, context: ViewContext):
        assert isinstance(context, ViewContext)
        if self.active_context:
            self.active_context.maps = self.view.maps()
        self.active_context = context
        self._sidebar.switch_context(context)
        self.view.show_maps(context)

    def visualize_variables(self, system_component: str, spatial_resolution: str, type_of_result: str,
                            result_to_view: str, filter_range: Tuple[float, float]) -> None:

        print("Reached visualize var")
        print(system_component)
        print(spatial_resolution)
        print(type_of_result)
        print(result_to_view)
        assert self.active_context is not None
        experiments = self.active_context.experiments
        count = len(experiments)
        assert count > 0
        tif_file_path_1 = experiments[0].result_path(system_component, spatial_resolution, type_of_result,
                                                     result_to_view)
        print("tif file 1:", tif_file_path_1)
        assert tif_file_path_1 is not None
        assert tif_file_path_1.exists()
        maps = self.view.maps()
        svc = MapService()
        svc.add_layer(maps[0], tif_file_path_1)
        if count == 2:
            tif_file_path_2 = experiments[1].result_path(system_component, spatial_resolution, type_of_result,
                                                         result_to_view)
            print("tif file 2:", tif_file_path_1)
            assert tif_file_path_2 is not None
            assert tif_file_path_2.exists()
            svc.add_layer(maps[1], tif_file_path_2)

    def onchange_tab(self, data):
        tab_index = data["new"]
        assert isinstance(tab_index, int)
        context = self.view.context(tab_index)
        self._switch_context(context)
