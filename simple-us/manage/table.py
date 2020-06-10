from __future__ import annotations
from typing import Any
from typing import List

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


class ExperimentTableView(Box):
    def __init__(self, controller: ExperimentTable):
        super(Box, self).__init__()

        self.controller = controller
        self.table = None
        self.build_table()

        self.children = [self.table]

    def build_table(self):
        self.table = vue.SimpleTable(children=[self.table_head()]) #,
                                               # self.table_body()])

    def table_head(self):
        titles = ["Select", "ID", "Name", "Status", "Description", "Delete"]
        header_cells = [vue.Col(children=[title]) for title in titles]
        # vue.DataTableHeader
        # vue.Header
        header_row = vue.Row(children=header_cells)
        # vue.Header
        # table_head = (children=[header_row])
        return header_row

    def table_body(self):
        pass
        experiment_rows = []
        for row_data in self.controller.experiments_row_data():
            row = self.experiment_row(row_data)
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows)
        return table_body

    def experiment_row(self, experiment_data: List[str]):
        # checkbox = mui.Html('
        # <span class="MuiButtonBase-root MuiIconButton-root PrivateSwitchBase-root-1 MuiCheckbox-root MuiCheckbox-colorSecondary PrivateSwitchBase-checked-2 Mui-checked MuiIconButton-colorSecondary" aria-disabled="false">
        # <span class="MuiIconButton-label">
        # <input class="PrivateSwitchBase-input-4" type="checkbox" data-indeterminate="false" aria-label="primary checkbox" value="" checked="">
        # <svg class="MuiSvgIcon-root" focusable="false" viewBox="0 0 24 24" aria-hidden="true">
        # <path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"> </path>
        # </svg>
        # </span>
        # <span class="MuiTouchRipple-root"></span>
        # </span>')
        checkbox = mui.Checkbox()
        # checkbox.ripple = True
        # checkbox.dark = True
        checkbox.background_color = "rgb(0, 0, 0, 0)"
        cells = [TableCell(children=checkbox)]
        cells += [TableCell(children=value) for value in experiment_data]
        delete_button = TableCell(children=mui.IconButton(children=mui.Icon(children="delete")))
        cells.append(delete_button)
        row = TableRow(children=cells, hover=True)
        checkbox.on_event("click", self.controller.onclick_experiment_row)
        delete_button.on_event("onClick", self.controller.onclick_delete)

        return row



class ExperimentTableViewMui(Box):
    def __init__(self, controller: ExperimentTable):
        super(Box, self).__init__()

        self.controller = controller
        self.table = None
        self.build_table()

        self.children = [self.table]

    def build_table(self):
        self.table = Table(children=[self.table_head(),
                                         self.table_body()],
                               color="primary.main")

    def table_head(self):
        titles = ["Select", "ID", "Name", "Status", "Description", "Delete"]
        header_cells = [TableCell(children=[title]) for title in titles]
        header_row = TableRow(children=header_cells)
        table_head = TableHead(children=[header_row])
        return table_head

    def table_body(self):
        experiment_rows = []
        for row_data in self.controller.experiments_row_data():
            row = self.experiment_row(row_data)
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows)
        return table_body

    def experiment_row(self, experiment_data: List[str]):
        # checkbox = mui.Html('
        # <span class="MuiButtonBase-root MuiIconButton-root PrivateSwitchBase-root-1 MuiCheckbox-root MuiCheckbox-colorSecondary PrivateSwitchBase-checked-2 Mui-checked MuiIconButton-colorSecondary" aria-disabled="false">
            # <span class="MuiIconButton-label">
                # <input class="PrivateSwitchBase-input-4" type="checkbox" data-indeterminate="false" aria-label="primary checkbox" value="" checked="">
                    # <svg class="MuiSvgIcon-root" focusable="false" viewBox="0 0 24 24" aria-hidden="true">
                        # <path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.11 0 2-.9 2-2V5c0-1.1-.89-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"> </path>
                    # </svg>
            # </span>
            # <span class="MuiTouchRipple-root"></span>
        # </span>')
        checkbox = mui.Checkbox()
        # checkbox.ripple = True
        # checkbox.dark = True
        checkbox.background_color = "rgb(0, 0, 0, 0)"
        cells = [TableCell(children=checkbox)]
        cells += [TableCell(children=value) for value in experiment_data]
        delete_button = TableCell(children=mui.IconButton(children=mui.Icon(children="delete")))
        cells.append(delete_button)
        row = TableRow(children=cells, hover=True)
        checkbox.on_event("click", self.controller.onclick_experiment_row)
        delete_button.on_event("onClick", self.controller.onclick_delete)

        return row


class ExperimentTable:
    def __init__(self):
        self.view = ExperimentTableView(self)
        self.selected_experiments_count = 0

    def experiments_row_data(self) -> List[List[str]]:
        return [
            [str(1), "Apple", "Pending", "-"],
            [str(2), "Orange", "Completed", "-"],
            [str(3), "Pear", "Failed", "-"]
        ]

    def onclick_experiment_row(self, widget, event, data):
        print(widget, event, data)
        print("checkbox")
        # for key, value in vars(widget).items():
        #     print(key, ":", value)
        # print("")
        # checkbox = widget.children[0].children
        # print(checkbox)
        # checkbox.checked = True

    def onclick_delete(self, widget, event, c):
        print("delete", widget, event, c)

    # def onclick_row(a, b, c):
    #     print(a, b, c)
    #     print(type(c))
    #     print("clicked row")
    #

    # row.on_event("onDoubleClick", click_handler)
    # display(table)
