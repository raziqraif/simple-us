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
        pass
