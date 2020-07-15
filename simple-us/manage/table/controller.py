from copy import copy
from typing import List, Optional

import ipymaterialui as mui
from ipymaterialui import TableRow

from ..details import Details
from database import DBManager
from utils import CustomCheckbox


class ExperimentTable:
    def __init__(self):
        from .view import ExperimentTableView
        self.view = ExperimentTableView(self)

        # Both the following attributes will be set externally by ManageTab
        self.create_experiment_chip = None  # A callback function to create a chip widget from id and name
        self.delete_experiment_chip = None  # A callback function to delete a chip widget from id

    def rows_data(self) -> List[List[str]]:
        db = DBManager()
        experiments = db.get_experiments()

        rows_data: List[List[str]] = []
        for exp in experiments:
            r_data = [exp.id_str, exp.name_str, exp.status_str, exp.description_str]
            rows_data.append(r_data)

        rows_data.append([
            "3", "Corn", "Pending", "Corn test data."
        ])
        rows_data.append([
            "4", "AllCrops", "Completed", "Allcrops test data."
        ])
        rows_data.append([
            "6", "A really long name for this experiment", "Completed",
            "A really long description for allcrops test data."
        ])

        return rows_data

    def selected_experiment_ids(self) -> [str]:
        """ Expose the view's method """

        return self.view.selected_experiment_ids()

    def selected_row_from_id(self, id_):
        """ Expose the view's method """

        return self.view.selected_row_from_id(id_)

    def toggle_row(self, row: TableRow):
        """ Expose the view's method """

        self.view.toggle_row(row)

    def onclick_row(self, widget, event, data, row: TableRow):
        self.view.toggle_row(row)

    def onclick_details(self, widget, event, data, job_id):
        details_window = Details().view
        without_details = copy(self.view.children)
        with_details = copy(self.view.children)
        with_details.append(details_window)
        self.view.children = with_details
