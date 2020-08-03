from copy import copy
from datetime import datetime
from typing import Callable, Optional

from ipymaterialui import Button
from pubsub import pub

from model import Experiment
from utils.misc import show_notification
from utils.pubsubmessage import sendMessage, NOTIFICATION_CREATED
from utils.widgets.notification import Notification
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
        pub.sendMessage(NOTIFICATION_CREATED, text="The table was refreshed", mode=Notification.SUCCESS,
                        page=Notification.MANAGE_PAGE)

    def onclick_display(self, widget: Button, event: str, data: dict):
        experiments = self.experiment_table.selected_experiments()

        assert len(experiments) <= 2
        if len(experiments) == 0:
            message = "Please select an experiment first."
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
            return
        elif len(experiments) == 2:
            message = "To view multiple experiments, click Compare"
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
            return

        experiment = experiments[0]
        if experiment is None:
            message = "Unexpected error occur."
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.ERROR, page=Notification.MANAGE_PAGE)
            return
        if not experiment.is_completed:
            message = "{} experiment cannot be displayed.".format(experiment.status_str)  # Failed/Pending experiment
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
            return

        if self.view_experiments(experiment, None):
            self.experiment_table.toggle_experiment_row(experiment.id_str)

    def onclick_compare(self, widget: Button, event: str, data: dict):
        experiments = self.experiment_table.selected_experiments()
        assert len(experiments) <= 2
        if len(experiments) == 0:
            message = "Please select an experiment first."
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
            return
        elif len(experiments) == 1:
            message = "To view a single experiment, click Display"
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
            return

        if None in experiments:
            message = "Unexpected error occur."
            sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.ERROR, page=Notification.MANAGE_PAGE)
            return
        for experiment in experiments:
            if not experiment.is_completed:
                # Failed/Pending experiment
                message = "{} experiment cannot be compared.".format(experiment.status_str)
                sendMessage(NOTIFICATION_CREATED, text=message, mode=Notification.WARNING, page=Notification.MANAGE_PAGE)
                return

        if self.view_experiments(experiments[0], experiments[1]):
            self.experiment_table.toggle_experiment_row(experiments[0].id_str)
            self.experiment_table.toggle_experiment_row(experiments[1].id_str)
