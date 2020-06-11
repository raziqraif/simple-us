from __future__ import annotations
from typing import Any
from typing import List
from typing import Union

import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipywidgets import Box
from ipymaterialui import Checkbox
from ipymaterialui import Table
from ipymaterialui import TableBody
from ipymaterialui import TableCell
from ipymaterialui import TableHead
from ipymaterialui import TableRow

from data import Experiment
from database import DBManager


class ExperimentTableView(Box):
    def __init__(self, controller: ExperimentTable):
        super(Box, self).__init__()

        self.controller = controller
        self.table = None
        self.build_table()

        self.children = [self.table]

    def build_table(self):
        self.table = Table(children=[self.table_head(),
                                     self.table_body()],
                           style_={"width": "1000px"})

    def table_head(self):
        titles = ["Select", "ID", "Name", "Status", "Description", "Delete"]
        header_cells = [TableCell(children=[title]) for title in titles]
        header_row = TableRow(children=header_cells)
        table_head = TableHead(children=[header_row])
        return table_head

    def table_body(self):
        experiment_rows = []
        for row_data in self.controller.rows_data():
            row = self.experiment_row(row_data)
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows)
        return table_body

    def experiment_row(self, experiment_data: List[str]):
        checkbox = mui.Checkbox(checked=False)
        delete_button = mui.IconButton(children=mui.Icon(children="delete"))

        # TODO: Improve style if given time
        checkbox_cell = TableCell(children=checkbox)
        id_cell = TableCell(children=experiment_data[0], style_={})
        name_cell = TableCell(children=experiment_data[1], style={})
        status_cell = TableCell(children=experiment_data[2], style={})
        description_cell = TableCell(children=experiment_data[3], style={"min_width": "100%"})
        delete_cell = TableCell(children=delete_button, style={})

        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            description_cell,
            delete_cell
        ]

        row = TableRow(children=cells, hover=True, selected=False, ripple=True)

        checkbox.on_event("onClick",
                          lambda widget, event, data:
                          self.controller.onclick_row(widget, event, data, checkbox, row))

        # for cell in cell

        # id_cell.on_event("onClick",
        #                  lambda widget, event, data:
        #                  self.controller.onclick_row(widget, event, data, checkbox, row))
        # name_cell.on_event("onClick",
        #                    lambda widget, event, data:
        #                    self.controller.onclick_row(widget, event, data, checkbox, row))
        # status_cell.on_event("onClick",
        #                      lambda widget, event, data:
        #                      self.controller.onclick_row(widget, event, data, checkbox, row))
        # description_cell.on_event("onClick",
        #                           lambda widget, event, data:
        #                           self.controller.onclick_row(widget, event, data, checkbox, row))
        #
        # id_cell.on_event("onDoubleClick",
        #                  lambda widget, event, data:
        #                  self.controller.ondoubleclick_row(widget, event, data))

        job_id = experiment_data[0]
        delete_button.on_event("onClick",
                               lambda widget, event, data:
                               self.controller.onclick_delete(widget, event, data, job_id))

        return row


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

        return rows_data

    def onclick_checkbox(self, widget: Checkbox, event, data, row_widget):
        widget.checked = not widget.checked
        row_widget.selected = not row_widget.selected

    def onclick_row(self, widget, event, data, checkbox, row):
        print("clicked row", widget, event, data,)
        row.selected = not row.selected
        checkbox.checked = not checkbox.checked

    def onclick_delete(self, widget, event, data, job_id):
        print("clicked delete", widget, event, data, job_id)

    def ondoubleclick_row(self, widget, event, data):
        print("double clicked row", widget, event, data)



















# checkbox = mui.Html('
# <span class="MuiButtonBase-root MuiIconButton-root PrivateSwitchBase-root-1 MuiCheckbox-root MuiCheckbox-colorSecondary PrivateSwitchBase-checked-2 Mui-checked MuiIconButton-colorSecondary" aria-disabled="false">
#     <span class="MuiIconButton-label">
#         <input class="PrivateSwitchBase-input-4" type="checkbox" data-indeterminate="false" aria-label="primary checkbox" value="" checked="">
#             <svg class="MuiSvgIcon-root" focusable="false" viewBox="0 0 24 24" aria-hidden="true">
#                 <path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"> </path>
#             </svg>
#     </span>
#     <span class="MuiTouchRipple-root"></span>
# </span>')
