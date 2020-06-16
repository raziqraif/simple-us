from __future__ import annotations
from typing import Any
from typing import List
from typing import Union

import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipymaterialui import Container
from ipymaterialui import Checkbox
from ipymaterialui import Icon
from ipymaterialui import IconButton
from ipymaterialui import Table
from ipymaterialui import TableBody
from ipymaterialui import TableCell
from ipymaterialui import TableHead
from ipymaterialui import TableRow

from data import Experiment
from database import DBManager
from utils import DEBUG_MODE
from utils import CustomText


class ExperimentTableView(Container):
    def __init__(self, controller: ExperimentTable):
        super(Container, self).__init__()

        self.style_ = {
            "width": "100%",
            "height": "300px",
            "padding": "0px 0px",
            # "size": "small"
        }
        self.controller = controller
        self.table = None
        self._build_table()

        self.children = [self.table]

    def _build_table(self):
        self.table = Table(children=[self._table_head(),
                                     self._table_body()],

                           size="small",
                           style_={
                               "width": "100%",
                               "padding": "0px 0px",
                           })

    def _table_head(self):
        titles = ["", "ID", "Name", "Status", "Description", "Delete"]

        select_cell = self._header_cell("", "50px")
        id_cell = self._header_cell("ID", "100px")
        name_cell = self._header_cell("Name", "120px")
        status_cell = self._header_cell("Status", "100px")
        description_cell = self._header_cell("Description", "")
        delete_cell = self._header_cell("Delete", "100px")

        header_cells = [select_cell,
                        id_cell,
                        name_cell,
                        status_cell,
                        description_cell,
                        delete_cell]

        header_row = TableRow(children=header_cells)
        table_head = TableHead(children=[header_row],
                               style_={
                                   "background": "#454851",
                               })
        return table_head

    def _table_body(self):
        experiment_rows = []
        for row_data in self.controller.rows_data():
            row = self._body_row(row_data)
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows,
                               style_={
                                   "padding": "0px 0px 0px 0px",
                               })

        return table_body

    def _header_cell(self, text, width) -> TableCell:
        cell = TableCell(children=CustomText(text),
                         size="small",
                         align="center",
                         style_={
                             "color": "#ffffff",
                             "padding": "0px 0px 0px 0px",
                             "height": "45px",
                             "width": width,
                         })
        return cell

    def _body_row(self, experiment_data: List[str]):
        checkbox = mui.Checkbox(checked=False,
                                style_={
                                    "width": "35px",
                                    "height": "35px",
                                })
        delete_icon = Icon(children="delete",
                           style_={
                               "font-size": "25px",
                               "padding": "0px 0px 0px 0px",
                           })
        delete_button = IconButton(children=delete_icon,
                                   style_={
                                       "padding": "0px 0px 0px 0px",
                                   })

        checkbox_cell = self._body_cell(checkbox, "60px", "center")
        id_cell = self._body_cell(CustomText(experiment_data[0]), "150px", "center")
        name_cell = self._body_cell(CustomText(experiment_data[1]), "150px", "left")
        status_cell = self._body_cell(CustomText(experiment_data[2]), "150px", "center")
        description_cell = self._body_cell("", "", "left")
        delete_cell = self._body_cell(delete_button, "60px", "center")

        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            description_cell,
            delete_cell
        ]

        row = TableRow(children=cells,
                       style_={
                           "padding": "0px 0px 0px 0px",
                       },
                       hover=True, selected=False, ripple=True)

        checkbox.on_event("onClick",
                          lambda widget, event, data:
                          self.controller.onclick_row(widget, event, data, checkbox, row))

        # for cell in cell
#         row.on_event("onClick",
#                          lambda widget, event, data:
#                          self.controller.onclick_row(widget, event, data, checkbox, row))

#         id_cell.on_event("onClick",
#                          lambda widget, event, data:
#                          self.controller.onclick_row(widget, event, data, checkbox, row))
#         checkbox_cell.on_event("onClick",
#                           lambda widget, event, data:
#                           self.controller.onclick_row(widget, event, data, checkbox, row))
#         name_cell.on_event("onClick",
#                            lambda widget, event, data:
#                            self.controller.onclick_row(widget, event, data, checkbox, row))
#         status_cell.on_event("onClick",
#                              lambda widget, event, data:
#                              self.controller.onclick_row(widget, event, data, checkbox, row))
#         description_cell.on_event("onClick",
#                                   lambda widget, event, data:
#                                   self.controller.onclick_row(widget, event, data, checkbox, row))
        
        id_cell.on_event("onDoubleClick",
                         lambda widget, event, data:
                         self.controller.ondoubleclick_row(widget, event, data))

        job_id = experiment_data[0]
        delete_button.on_event("onClick",
                               lambda widget, event, data:
                               self.controller.onclick_delete(widget, event, data, job_id))

        return row

    def _body_cell(self, children, width, align) -> TableCell:
        cell = TableCell(children=children,
                         align=align,
                         style_={
                             "padding": "0px 0px 0px 0px",
                             "width": width,
                             "height": "45px",
                         })
        return cell


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
        if DEBUG_MODE:
            print("clicked row", widget, event, data,)
        row.selected = not row.selected
        checkbox.checked = not checkbox.checked

    def onclick_delete(self, widget, event, data, job_id):
        if DEBUG_MODE:
            print("clicked delete", widget, event, data, job_id)

    def ondoubleclick_row(self, widget, event, data):
        if DEBUG_MODE:
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
