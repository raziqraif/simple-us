from copy import copy
from typing import List, Optional

import ipymaterialui as mui
from ipymaterialui import TableRow

from model import Experiment
from ..detailsdialog import Details
from database import DBManager
from utils import CustomCheckbox


class ExperimentTable:
    def __init__(self):
        from .view import ExperimentTableView
        self.view: ExperimentTableView = ExperimentTableView(self)

        # Both the following attributes will be set externally by ManageTab
        self.create_experiment_chip = None  # A callback function to create a chip widget from id and name
        self.delete_experiment_chip = None  # A callback function to delete a chip widget from id

    def load_experiments(self) -> List[Experiment]:
        db = DBManager()
        experiments = db.get_experiments()
        return experiments

    def selected_experiments(self) -> List[Optional[Experiment]]:
        id_strs = self.view.selected_experiments_id_str()
        experiments = [Experiment.from_id_str(id_str) for id_str in id_strs]
        return experiments

    def toggle_experiment_row(self, id_str: str):
        row = self.view.selected_row_from_id_str(id_str)
        self.view.toggle_row(row)

    def onclick_row(self, widget, event, data, row: TableRow):
        self.view.toggle_row(row)

    def onclick_details(self, widget, event, data, job_id):
        details_window = Details().view
        without_details = copy(self.view.children)
        with_details = copy(self.view.children)
        with_details.append(details_window)
        self.view.children = with_details
