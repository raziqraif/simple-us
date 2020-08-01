from typing import List, Optional

from model.variableutil import VariableService
from ..viewcontext import ViewContext
from model import Experiment


DEFAULT_SELECTION = "Select"


class Sidebar:
    def __init__(self):
        from .view import SidebarView
        self.view = SidebarView(self)
        self.context: Optional[ViewContext] = None
        self.visualize_variables_callback = None  # LOOKATME: Callback function. Must be set externally.
        self.close_tab_callback = None  # LOOKATME: Callback function. Must be set externally

    @property
    def experiments(self) -> List[Experiment]:
        return self.context.experiments if self.context is not None else []

    def switch_context(self, context: Optional[ViewContext]):
        if self.context:
            self.context.system_component = self.view.system_component
            self.context.spatial_resolution = self.view.spatial_resolution
            self.context.type_of_result = self.view.type_of_result
            self.context.result_to_view = self.view.result_to_view
            self.context.filter_min = self.view.filter_min
            self.context.filter_max = self.view.filter_max
        self.context = context
        if context is not None:
            self._refresh_options()
            self._refresh_selections()

    def onchange_system_components(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.view.set_spatial_resolution(DEFAULT_SELECTION)
            self._update_spatial_resolution_options()

    def onchange_spatial_resolution(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.view.set_type_of_result(DEFAULT_SELECTION)
            self._update_type_of_result_options()

    def onchange_type_of_results(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.view.set_result_to_view(DEFAULT_SELECTION)
            self._update_result_to_view_options()

    def onchange_filter_range(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            old_min, old_max = [int(value) for value in change['old']]
            min_, max_ = [int(value) for value in change['new']]
            if min_ != max_:
                self.view.set_filter_range(min_, max_)
                return
            if min_ == old_min:
                max_ += 1
            elif max_ == old_max:
                min_ -= 1
            elif max_ != 0:
                min_ = max_ - 1
            elif min_ != 100:
                max_ = min_ + 1
            self.view.set_filter_range(min_, max_)

    def onclick_visualize(self, widget, event, data):
        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        type_of_res = self.view.type_of_result
        res_to_view = self.view.result_to_view
        filter_min = self.view.filter_range[0]
        filter_max = self.view.filter_range[1]

        # TODO: Show error message
        if sys_comp == DEFAULT_SELECTION:
            return
        if spat_res == DEFAULT_SELECTION:
            return
        if type_of_res == DEFAULT_SELECTION:
            return
        if res_to_view == DEFAULT_SELECTION:
            return
        if filter_min == filter_max:
            return

        assert self.visualize_variables_callback is not None
        self.visualize_variables_callback(sys_comp, spat_res, type_of_res, res_to_view, filter_min, filter_max)

    def onclick_csv(self, widget, event, data):
        pass

    def onclick_close(self, widget, event, data):
        assert self.context is not None
        assert self.close_tab_callback is not None
        self.close_tab_callback(self.context)

    def _refresh_selections(self):
        self.view.set_system_component(self.context.system_component)
        self.view.set_spatial_resolution(self.context.spatial_resolution)
        self.view.set_type_of_result(self.context.type_of_result)
        self.view.set_result_to_view(self.context.result_to_view)
        self.view.set_filter_range(self.context.filter_min, self.context.filter_max)

    def _refresh_options(self):
        self._update_system_components_options()
        self._update_spatial_resolution_options()
        self._update_type_of_result_options()
        self._update_result_to_view_options()

    def _update_system_components_options(self):
        options = [DEFAULT_SELECTION]

        if len(self.experiments) == 0:
            return
        options += self.context.variable_service.system_component_options()
        self.view.update_system_component_options(options)

    def _update_spatial_resolution_options(self):
        options = [DEFAULT_SELECTION]
        sys_comp = self.view.system_component
        if sys_comp == DEFAULT_SELECTION:
            self.view.update_spatial_resolution_options(options)
            return

        if len(self.experiments) == 0:
            return
        options += self.context.variable_service.spatial_resolution_options(sys_comp)
        self.view.update_spatial_resolution_options(options)

    def _update_type_of_result_options(self):
        options = [DEFAULT_SELECTION]

        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        if sys_comp == DEFAULT_SELECTION or spat_res == DEFAULT_SELECTION:
            self.view.update_type_of_results_options(options)
            return

        if len(self.experiments) == 0:
            return
        options += self.context.variable_service.type_of_result_options(sys_comp, spat_res)
        self.view.update_type_of_results_options(options)

    def _update_result_to_view_options(self):
        options = [DEFAULT_SELECTION]

        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        type_of_res = self.view.type_of_result

        if sys_comp == DEFAULT_SELECTION or spat_res == DEFAULT_SELECTION or type_of_res == DEFAULT_SELECTION:
            self.view.update_result_to_view_options(options)
            return

        if len(self.experiments) == 0:
            return
        options += self.context.variable_service.result_to_view_options(sys_comp, spat_res, type_of_res)

        self.view.update_result_to_view_options(options)
