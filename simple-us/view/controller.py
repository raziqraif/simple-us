from typing import List
from typing import Optional
from typing import Tuple

from .context import ViewContext
from .sidebar import Sidebar
from model import Experiment


class ViewTab:
    def __init__(self):
        from .view import ViewTabUI
        self._sidebar = Sidebar()
        self._sidebar.visualize_variables = self.visualize_variables
        self.contexts: List[ViewContext] = []
        self.active_context: Optional[ViewContext] = None

        self.view = ViewTabUI(self, self._sidebar.view)

    @property
    def active_tab_model(self) -> any:
        return self.active_context

    def maps_from_model(self, tab_model: any) -> any:
        assert isinstance(tab_model, ViewContext)
        return tab_model.maps

    def map_titles_from_model(self, tab_model: any) -> List[str]:
        assert isinstance(tab_model, ViewContext)
        return tab_model.map_titles

    def save_maps_to_model(self, maps: List[any], tab_model: any):
        assert isinstance(tab_model, ViewContext)
        tab_model.maps = maps

    def new_view(self, experiments: List[Experiment]):
        """ New display/compare view"""

        context = ViewContext(experiments)
        self.contexts.append(context)
        self._switch_context(context)
        self.view.new_tab(context.title, context, context.is_comparison)

    def _switch_context(self, context: ViewContext):
        self._sidebar.switch_context(context)
        if self.active_context:
            self.active_context.maps = self.view.maps()
        self.active_context = context

    def visualize_variables(self, system_component: str, spatial_resolution: str, type_of_result: str,
                            result_to_view: str, filter_range: Tuple[float, float]) -> None:
        assert self.active_context is not None
        experiments = self.active_context.experiments
        count = len(experiments)
        assert count > 0
        tif_file_path_1 = experiments[0].result_path(system_component, spatial_resolution, type_of_result,
                                                     result_to_view)
        assert tif_file_path_1 is not None
        assert tif_file_path_1.exists()
        if count == 2:
            tif_file_path_2 = experiments[1].result_path(system_component, spatial_resolution, type_of_result,
                                                         result_to_view)
            assert tif_file_path_2 is not None
            assert tif_file_path_2.exists()

