from copy import copy

from ipymaterialui import Button

from model import Experiment
from .table import ExperimentTable
from utils import ExperimentChip


class ManageTab:
    def __init__(self, view_experiments_callback):
        from .view import ManageTabView
        self.experiment_table = ExperimentTable()
        self.view = ManageTabView(self, self.experiment_table.view)
        self.experiment_table.create_experiment_chip = self.view.append_chip
        self.experiment_table.delete_experiment_chip = self.view.remove_chip

        self.view_experiments = view_experiments_callback  # Function callback. Accepts a list of Experiment objects.
        # Must be set externally by the App class

    def ondelete_chip(self, widget: ExperimentChip, event, data):
        experiment_id = widget.experiment_id
        associated_row = self.experiment_table.selected_row_from_id(experiment_id)

        if associated_row:
            self.experiment_table.toggle_row(associated_row)
            # experiment_table have access to the create/delete experiment chip widget API. The chip widget removal will
            # be done there.

    def onclick_refresh(self, widget: Button, event: str, data: dict):
        pass

    def onclick_display(self, widget: Button, event: str, data: dict):
        ids = self.experiment_table.selected_experiment_ids()
        assert len(ids) <= 2
        if len(ids) == 0:
            return  # TODO: Display error message
        elif len(ids) == 2:
            return  # TODO: Display error message
        experiment = Experiment.from_id_str(ids[0])
        if experiment is None:
            return  # TODO: display error message
        if not experiment.is_completed:
            return  # TODO: display error message

        self.view_experiments([experiment])

    def onclick_compare(self, widget: Button, event: str, data: dict):
        ids = self.experiment_table.selected_experiment_ids()
        assert len(ids) <= 2
        if len(ids) == 0:
            return  # TODO: Display error message
        elif len(ids) == 1:
            return  # TODO: Display error message

        experiments = [Experiment.from_id_str(id_str) for id_str in ids]
        if None in experiments:
            return  # TODO: display error message
        for exp in experiments:
            if not exp.is_completed:
                return  # TODO: error message

        # TODO: Make sure result lists intersect
        self.view_experiments(experiments)
