from copy import copy
from datetime import datetime
from typing import Callable, Optional

from ipymaterialui import Button
from pubsub import pub

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

        self.view_experiments: Callable[[Experiment, Optional[Experiment]], bool] = view_experiments_callback

    def ondelete_chip(self, widget: ExperimentChip, event, data):
        self.experiment_table.toggle_experiment_row(widget.experiment_id_str)

        # experiment_table have access to the create/delete experiment chip widget API.
        # The chip widget removal will be done there.

    def onclick_refresh(self, widget: Button, event: str, data: dict):
        from utils.pubsubmessage import REFRESH_BUTTON_CLICKED
        pub.sendMessage(REFRESH_BUTTON_CLICKED)

    def onclick_display(self, widget: Button, event: str, data: dict):
        experiments = self.experiment_table.selected_experiments()
        assert len(experiments) <= 2
        if len(experiments) == 0:
            return  # TODO: Display error message
        elif len(experiments) == 2:
            return  # TODO: Display error message

        experiment = experiments[0]
        if experiment is None:
            return  # TODO: display error message
        if not experiment.is_completed:
            return  # TODO: display error message

        if self.view_experiments(experiment, None):
            self.experiment_table.toggle_experiment_row(experiment.id_str)

    def onclick_compare(self, widget: Button, event: str, data: dict):
        experiments = self.experiment_table.selected_experiments()
        assert len(experiments) <= 2
        if len(experiments) == 0:
            return  # TODO: Display error message
        elif len(experiments) == 1:
            return  # TODO: Display error message

        if None in experiments:
            return  # TODO: display error message
        for exp in experiments:
            if not exp.is_completed:
                return  # TODO: error message

        # TODO: Make sure result lists intersect
        if self.view_experiments(experiments[0], experiments[1]):
            self.experiment_table.toggle_experiment_row(experiments[0].id_str)
            self.experiment_table.toggle_experiment_row(experiments[1].id_str)
