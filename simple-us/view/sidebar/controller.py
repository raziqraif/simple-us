from typing import List, Optional

from ..context import ViewContext
from model import Experiment


class Sidebar:
    def __init__(self):
        from .view import SidebarView
        self.view = SidebarView(self)
        self.context: Optional[ViewContext] = None
        self.visualize_variables = None  # Callback function. Must be set externally

    @property
    def experiments(self) -> List[Experiment]:
        return self.context.experiments if self.context is not None else []

    def refresh(self):
        self._update_system_components_options()
        self._update_spatial_resolution_options()
        self._update_type_of_result_options()
        self._update_result_to_view_options()

    def switch_context(self, context: ViewContext):
        if self.context:
            self.context.system_component = self.view.system_component
            self.context.spatial_resolution = self.view.spatial_resolution
            self.context.type_of_result = self.view.type_of_result
            self.context.result_to_view = self.view.result_to_view
        self.context = context
        self.refresh()

    def _update_system_components_options(self):
        options = ["Select"]

        if len(self.experiments) == 0:
            return
        experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.system_component_options()
        elif len(self.experiments) == 2:
            experiment_2 = self.experiments[1]
            intersected_paths = experiment.intersect_result_paths(experiment_2)
            options += experiment.system_component_options(intersected_paths)

        self.view.update_system_component_options(options)

    def _update_spatial_resolution_options(self):
        options = ["Select"]
        sys_comp = self.view.system_component
        if sys_comp == "Select":
            self.view.update_spatial_resolution_options(options)
            return

        if len(self.experiments) == 0:
            return
        experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.spatial_resolution_options(sys_comp)
        elif len(self.experiments) == 2:
            experiment_2 = self.experiments[1]
            intersected_paths = experiment.intersect_result_paths(experiment_2)
            options += experiment.spatial_resolution_options(sys_comp, intersected_paths)

        self.view.update_spatial_resolution_options(options)

    def _update_type_of_result_options(self):
        options = ["Select"]

        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        if sys_comp == "Select" or spat_res == "Select":
            self.view.update_type_of_results_options(options)
            return

        if len(self.experiments) == 0:
            return
        experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.type_of_result_options(sys_comp, spat_res)
        elif len(self.experiments) == 2:
            experiment_2 = self.experiments[1]
            intersected_paths = experiment.intersect_result_paths(experiment_2)
            options += experiment.type_of_result_options(sys_comp, spat_res, intersected_paths)

        self.view.update_type_of_results_options(options)

    def _update_result_to_view_options(self):
        options = ["Select"]

        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        type_of_res = self.view.type_of_result

        if sys_comp == "Select" or spat_res == "Select" or type_of_res == "Select":
            self.view.update_result_to_view_options(options)
            return

        if len(self.experiments) == 0:
            return
        experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.result_to_view_options(sys_comp, spat_res, type_of_res)
        elif len(self.experiments) == 2:
            experiment_2 = self.experiments[1]
            intersected_paths = experiment.intersect_result_paths(experiment_2)
            options += experiment.result_to_view_options(sys_comp, spat_res, type_of_res, intersected_paths)

        # experiment = self.experiments[0]
        # result_list = experiment.result_list
        # options += [result_list[sys_comp][spat_res][key] for key in result_list[sys_comp][spat_res].keys()][0]

        self.view.update_result_to_view_options(options)

    def onchange_system_components(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self._update_spatial_resolution_options()

    def onchange_spatial_resolution(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self._update_type_of_result_options()

    def onchange_type_of_results(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self._update_result_to_view_options()

    def onclick_visualize(self, widget, event, data):
        sys_comp = self.view.system_component
        spat_res = self.view.spatial_resolution
        type_of_res = self.view.type_of_result
        res_to_view = self.view.result_to_view

        # TODO: Show error message
        if sys_comp == "Select":
            return
        if spat_res == "Select":
            return
        if type_of_res == "Select":
            return
        if res_to_view == "Select":
            return

        assert self.visualize_variables is not None
        self.visualize_variables(sys_comp, spat_res, type_of_res, res_to_view, self.view.filter_range)

    def onclick_csv(self, widget, event, data):
        pass
