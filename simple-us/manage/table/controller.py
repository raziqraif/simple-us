import threading
from copy import copy
from datetime import datetime
from typing import List, Optional

import ipymaterialui as mui
from ipymaterialui import TableRow

from model import Experiment
from ..detailsdialog import Details
from database import DBManager
from utils import CustomCheckbox
from utils.pubsubmessage import sendMessage, DETAILS_WINDOW_CLOSED, DATABASE_MODIFIED
from utils.pubsubmessage import subscribe
from utils.pubsubmessage import REFRESH_BUTTON_CLICKED


class ExperimentTable:
    def __init__(self):
        self._last_db_load = None
        from .view import ExperimentTableView
        self.view: ExperimentTableView = ExperimentTableView(self)

        # Both the following attributes will be set externally by ManageTab
        self.create_experiment_chip = None  # A callback function to create a chip widget from id and name
        self.delete_experiment_chip = None  # A callback function to delete a chip widget from id

        subscribe(self._handle_refresh_experiments, REFRESH_BUTTON_CLICKED)
        subscribe(self._handle_database_modified, DATABASE_MODIFIED)
        subscribe(self._handle_details_window_closed, DETAILS_WINDOW_CLOSED)

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

    def _handle_details_window_closed(self):
        self.view.children = copy(self.view.children)[:-1]

    def onclick_row(self, widget, event, data, row):
        from .view import TableRowWithExperiment
        assert isinstance(row, TableRowWithExperiment)
        self.view.toggle_row(row)

    def onclick_details(self, widget, event, data, job_id_str: str):
        experiment = Experiment.from_id_str(job_id_str)
        if experiment is None:

            return
        details_window = Details(experiment).view
        without_details = copy(self.view.children)
        for widget in without_details:
            print(str(widget)[:6])
        with_details = copy(self.view.children)
        with_details.append(details_window)
        print("len with details", len(with_details))
        self.view.children = with_details
