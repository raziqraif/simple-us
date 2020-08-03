import threading
from copy import copy
from datetime import datetime
from typing import List, Optional

import ipymaterialui as mui
from ipymaterialui import TableRow

from model import Experiment
from utils.widgets.notification import Notification
from ..detailsdialog import Details
from database import DBManager
from utils import CustomCheckbox
from utils.pubsubmessage import sendMessage, DETAILS_WINDOW_CLOSED, DATABASE_MODIFIED, NOTIFICATION_CREATED
from utils.pubsubmessage import subscribe
from utils.pubsubmessage import REFRESH_BUTTON_CLICKED


class ExperimentTable:
    def __init__(self):
        self._last_db_load = None
        from .view import ExperimentTableView
        self.details_window = Details(None)
        self.view: ExperimentTableView = ExperimentTableView(self, details_window=self.details_window.view)

        # Both the following attributes will be set externally by ManageTab
        self.create_experiment_chip = None  # A callback function to create a chip widget from id and name
        self.delete_experiment_chip = None  # A callback function to delete a chip widget from id

        subscribe(self._handle_refresh_experiments, REFRESH_BUTTON_CLICKED)
        subscribe(self._handle_database_modified, DATABASE_MODIFIED)

    def load_experiments(self) -> List[Experiment]:
        db = DBManager()
        experiments = db.get_experiments()
        self._last_db_load = datetime.now()
        return experiments

    def selected_experiments(self) -> List[Optional[Experiment]]:
        rows = self.view.selected_rows
        experiments = [row.experiment for row in rows]
        return experiments

    def toggle_experiment_row(self, id_str: str):
        row = self.view.selected_row_from_id_str(id_str)
        self.view.toggle_row(row)

    def _handle_refresh_experiments(self):
        if (self._last_db_load is None) or (DBManager.last_modified() > self._last_db_load):
            self.view.refresh_table()
        else:
            self.view.deselect_selected_rows()
            self.view.sort_table(default=True)

    def _handle_database_modified(self):
        if (self._last_db_load is None) or (DBManager.last_modified() > self._last_db_load):
            self.view.refresh_table()

    def onclick_row(self, widget, event, data, row):
        from .view import TableRowWithExperiment
        assert isinstance(row, TableRowWithExperiment)
        self.view.toggle_row(row)

    def onclick_details(self, widget, event, data, experiment: Experiment):
        if experiment is None:
            sendMessage(NOTIFICATION_CREATED, text="Unexpected error occured", mode=Notification.ERROR,
                        page=Notification.MANAGE_PAGE)
            return
        self.details_window.show(experiment)
