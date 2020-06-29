from __future__ import annotations

from copy import copy
from typing import List, Optional

import ipymaterialui as mui
from ipymaterialui import TableRow

from .view import ExperimentTableView
from ..details import Details
from database import DBManager
from utils import CustomCheckbox


class ExperimentTable:
    def __init__(self, create_chip_callback=None, delete_chip_callback=None):
        self.view = ExperimentTableView(self)
        self.selected_rows = []
        self._create_experiment_chip = create_chip_callback  # A callback function to create a chip widget from id
        # and name
        self._delete_experiment_chip = delete_chip_callback  # A callback function to delete a chip widget from id

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

    @property
    def create_experiment_chip(self):
        if self._create_experiment_chip:
            return self._create_experiment_chip
        return lambda experiment_id, experiment_name: None

    @create_experiment_chip.setter
    def create_experiment_chip(self, callback):
        self._create_experiment_chip = callback

    @property
    def delete_experiment_chip(self):
        if self._delete_experiment_chip:
            return self._delete_experiment_chip
        return lambda experiment_id: None

    @delete_experiment_chip.setter
    def delete_experiment_chip(self, callback):
        self._delete_experiment_chip = callback

    def checkbox_from_row(self, row: TableRow) -> CustomCheckbox:
        checkbox_cell = row.children[0]
        checkbox = checkbox_cell.children
        return checkbox

    def name_from_row(self, row: TableRow) -> str:
        name_cell = row.children[2]
        name_div = name_cell.children
        name = name_div.children
        return name.strip()

    def id_from_row(self, row: TableRow) -> str:
        id_cell = row.children[1]
        id_div = id_cell.children
        id = id_div.children
        return id.strip()

    def selected_row_with_id(self, experiment_id) -> Optional[TableRow]:
        experiment_id = experiment_id.strip()
        for row in self.selected_rows:
            id_in_row = self.id_from_row(row)
            if id_in_row == experiment_id:
                return row
        return None

    def select_row(self, row: TableRow) -> None:
        checkbox = self.checkbox_from_row(row)
        checkbox.checked = True
        row.selected = True
        self.selected_rows.append(row)

    def deselect_row(self, row: TableRow) -> None:
        checkbox = self.checkbox_from_row(row)
        checkbox.checked = False
        row.selected = False
        self.selected_rows.remove(row)

    def onclick_row(self, widget, event, data, row: TableRow):
        checkbox = self.checkbox_from_row(row)
        if not checkbox.checked:
            if len(self.selected_rows) >= 2:
                # TODO: Replace this with a snickbar.
                # print("You can only select the maximum of 2 experiments at a time.")
                return
            else:
                self.select_row(row)
                name = self.name_from_row(row)
                id_ = self.id_from_row(row)
                self.create_experiment_chip(id_, name)
        elif checkbox.checked:
            self.deselect_row(row)
            id_ = self.id_from_row(row)
            self.delete_experiment_chip(id_)

    def onclick_details(self, widget, event, data, job_id):
        details_window = Details().view
        without_details = copy(self.view.children)
        with_details = copy(self.view.children)
        with_details.append(details_window)
        self.view.children = with_details

