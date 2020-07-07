from typing import List

from model import Experiment


class Sidebar:
    def __init__(self):
        from .view import SidebarView
        self.view = SidebarView(self)
        self.experiments: List[Experiment] = []

    def update_system_components_options(self):
        options = ["Select"]

        experiment = None
        if len(self.experiments) != 0:
            experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.system_component_options()
        # elif len(self.experiments) == 2:
        #     options += experiment.system_component_options()

        self.view.update_system_components_options(options)

    def update_spatial_resolution_options(self):
        options = ["Select"]
        sys_comp = self.view.system_components_value()
        if sys_comp == "Select":
            self.view.update_spatial_resolution_options(options)
            return

        experiment = None
        if len(self.experiments) != 0:
            experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.spatial_resolution_options(sys_comp)
        # elif len(self.experiments) == 2:
        #     options += experiment.system_component_options(sys_comp)

        self.view.update_spatial_resolution_options(options)

    def update_type_of_results_options(self):
        options = ["Select"]

        sys_comp = self.view.system_components_value()
        spat_res = self.view.spatial_resolution_value()
        if sys_comp == "Select" or spat_res == "Select":
            self.view.update_type_of_results_options(options)
            print("return type of res")
            return

        experiment = None
        if len(self.experiments) != 0:
            experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.type_of_result_options(sys_comp, spat_res)
        # elif len(self.experiments) == 2:
        #     options += experiment.system_component_options(sys_comp)

        self.view.update_type_of_results_options(options)

    def update_result_to_view_options(self):
        options = ["Select"]

        sys_comp = self.view.system_components_value()
        spat_res = self.view.spatial_resolution_value()
        type_of_res = self.view.type_of_results_value()

        if sys_comp == "Select" or spat_res == "Select" or type_of_res == "Select":
            self.view.update_result_to_view_options(options)
            print("return res to view")
            return

        experiment = None
        if len(self.experiments) != 0:
            experiment = self.experiments[0]
        if len(self.experiments) == 1:
            options += experiment.result_to_view_options(sys_comp, spat_res, type_of_res)

        # experiment = self.experiments[0]
        # result_list = experiment.result_list
        # options += [result_list[sys_comp][spat_res][key] for key in result_list[sys_comp][spat_res].keys()][0]

        self.view.update_result_to_view_options(options)

    def refresh(self):
        self.update_system_components_options()
        self.update_spatial_resolution_options()
        self.update_type_of_results_options()
        self.update_result_to_view_options()

    def onchange_system_components(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.update_spatial_resolution_options()

    def onchange_spatial_resolution(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.update_type_of_results_options()

    def onchange_type_of_results(self, change):
        if change['name'] == 'value' and (change['new'] != change['old']):
            self.update_result_to_view_options()

    def onclick_visualize(self, widget, event, data):
        pass

    def onclick_csv(self, widget, event, data):
        pass
