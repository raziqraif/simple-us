from __future__ import annotations
from typing import List

from ipymaterialui import TableRow

from database import DBManager
from manage.table import ExperimentTableView
from utils import CustomCheckbox
from utils import DEBUG_MODE


class ExperimentTable:
    def __init__(self):
        self.view = ExperimentTableView(self)
        self.selected_rows_count = 0

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
            "5", "WWWWWWWWW", "Completed", "Allcrops test data."
        ])

        return rows_data

    def onclick_row(self, widget, event, data, row_widget: TableRow, checkbox_widget: CustomCheckbox):
        print("entered checkbox handler. Checked = ", checkbox_widget.checked)
        if not checkbox_widget.checked:
            if self.selected_rows_count >= 2:
                # TODO: Replace this with a toast.
                print("You can only select the maximum of 2 experiments at a time.")
                return
            else:
                self.selected_rows_count += 1
        if checkbox_widget.checked:
            self.selected_rows_count -= 1

        checkbox_widget.checked = not checkbox_widget.checked
        row_widget.selected = not row_widget.selected

    def onclick_details(self, widget, event, data, job_id):
        print("clicked details", widget, event, data, job_id)