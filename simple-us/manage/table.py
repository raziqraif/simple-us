from __future__ import annotations
from typing import Any
from typing import List
from typing import Union

import ipymaterialui as mui
import ipyvuetify as vue
import ipywidgets as widgets
from ipymaterialui import Container
from ipymaterialui import Checkbox
from ipymaterialui import Html
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
        # Table is split into two because stickyHeader property doesn't seem to work.
        # TODO: Fix the above error if given time.
        self.table_container = None
        self.table_for_header = None
        self.table_for_body_w_container = None
        self._build_table()

        # TODO: Discuss with Jungha which approach is more favorable
        # self.children = [self.table_for_header,
        #                  self.table_for_body_w_container]
        self.children = [self.table_container]

    def rows(self):
        rows = []
        # body = self.table.children[0]:

    def _build_table(self):
        head = self._table_head()
        body = self._table_body()
        self.table_for_header = Table(children=[head],
                                      size="small",
                                      style_={
                                          "width": "100%",
                                          "padding": "0px 0px",
                                      })
        table_for_body = Table(children=[body],
                               size="small",
                               style_={
                                   "width": "100%",
                                   "padding": "0px 0px",
                               })
        self.table_for_body_w_container = Container(children=[table_for_body],
                                                    style_={
                                                      "width": "100%",
                                                      "maxHeight": "650px",
                                                      "overflow": "auto",
                                                      "padding": "0px 0px 0px 0px",
                                                  })

        self.table = Table(children=[head, body])
        self.table_container = Container(children=[self.table],
                                         style_={
                                             "width": "100%",
                                             "maxHeight": "650px",
                                             "overflow": "auto",
                                             "padding": "0px 0px 0px 0px",
                                         })

    def _table_head(self):
        select_cell = self._header_cell("", "60px")
        id_cell = self._header_cell("ID", "150px")
        name_cell = self._header_cell("Name", "150px")
        status_cell = self._header_cell("Status", "150px")
        description_cell = self._header_cell("Description", "")
        details_cell = self._header_cell("", "60px")
        # details_cell = self._header_cell("", "77px")

        header_cells = [select_cell,
                        id_cell,
                        name_cell,
                        status_cell,
                        description_cell,
                        details_cell]

        header_row = TableRow(children=header_cells,
                              style_={
                                  "padding": "0px 10px 0px 30px",
                              })
        table_head = TableHead(children=[header_row],
                               sticky_header=True,
                               style_={
                                   "position": "sticky",
                                   "width": "100%",
                                   "background": "#454851",
                               })
        return table_head

    def _table_body(self):
        experiment_rows = []
        for row_data in self.controller.rows_data():
            row = self._body_row(row_data)
            experiment_rows.append(row)
        while len(experiment_rows) < 20:
            row = self._empty_body_row()
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows,
                               style_={
                                   "width": "100%",
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
        cell = Html(children=CustomText(text),
                    tag="th",
                    style_={
                        "color": "#ffffff",
                        "padding": "0px 0px 0px 0px",
                        "height": "45px",
                        "width": width,
                        "position": "sticky",
                        "background": "#454851",
                    })
        return cell

    def _body_row(self, experiment_data: List[str]):
        checkbox = mui.Checkbox(checked=False,
                                style_={
                                    "padding": "8px 8px 8px 8px",
                                    "width": "35px",
                                    "height": "35px",
                                })
        details_icon = Icon(children="open_in_new",
                            style_={
                                "font-size": "20px",
                                "padding": "0px 0px 0px 0px",
                            })
        details_button = IconButton(children=details_icon,
                                    style_={
                                        "padding": "8px 8px 8px 8px",
                                    })

        # TODO: Move delete button to popup window
        delete_icon = Icon(children="delete",
                           style_={
                               "font-size": "25px",
                               "padding": "0px 0px 0px 0px",
                           })
        delete_button = IconButton(children=delete_icon,
                                   style_={
                                       "padding": "8px 8px 8px 8px",
                                   })

        checkbox_cell = self._body_cell(checkbox, "60px", "center")
        id_cell = self._body_cell(CustomText(experiment_data[0]), "150px", "center")
        name_cell = self._body_cell(CustomText(experiment_data[1]), "150px", "left")
        status_cell = self._body_cell(CustomText(experiment_data[2]), "150px", "center")
        description_cell = self._body_cell("", "", "left")
        details_cell = self._body_cell(details_button, "60px", "center")

        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            description_cell,
            details_cell
        ]

        row = TableRow(children=cells,
                       style_={
                           "padding": "0px 0px 0px 0px",
                       },
                       hover=True, selected=False, ripple=True)

        checkbox.on_event("onClick",
                          lambda widget, event, data:
                          self.controller.onclick_checkbox(widget, event, data, row, checkbox))

        job_id = experiment_data[0]
        details_button.on_event("onClick",
                                lambda widget, event, data:
                                self.controller.onclick_details(widget, event, data, job_id))

        return row

    def _empty_body_row(self):
        checkbox_cell = self._body_cell("", "60px", "center")
        id_cell = self._body_cell("", "150px", "center")
        name_cell = self._body_cell("", "150px", "left")
        status_cell = self._body_cell("", "150px", "center")
        description_cell = self._body_cell("", "", "left")
        details_cell = self._body_cell("", "60px", "center")
        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            description_cell,
            details_cell
        ]
        row = TableRow(children=cells,
                       style_={
                           "padding": "0px 0px 0px 0px",
                       },
                       hover=False, selected=False, ripple=True)
        return row

    def _body_cell(self, children, width, align) -> TableCell:
        cell = TableCell(children=children,
                         align=align,
                         style_={
                             "padding": "0px 8px 0px 8px",
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

    def empty_callback(self):
        print("entered empty handler")
        # pass

    def onclick_checkbox(self, widget: Checkbox, event, data, row_widget, checkbox):
        print("entered checkbox handler. Checked = ", checkbox.checked)
        # if data is None:
        #     return
        if not checkbox.checked:
            if self.selected_rows_count >= 1:
                print("You can only select the maximum of 2 experiments at a time.")
                checkbox.checked = False
                checkbox.send_state("checked")
                checkbox.get_state()
                return
            else:
                self.selected_rows_count += 1
        if checkbox.checked:
            self.selected_rows_count -= 1

        checkbox.checked = not checkbox.checked
        row_widget.selected = not row_widget.selected
        checkbox.send_state("checked")

    def onclick_details(self, widget, event, data, job_id):
        if DEBUG_MODE:
            print("clicked details", widget, event, data, job_id)

    def ondoubleclick_row(self, widget, event, data):
        # TODO: Deprecate this?
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
