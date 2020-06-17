from __future__ import annotations
from typing import List

from ipymaterialui import Container
from ipymaterialui import Html
from ipymaterialui import Icon
from ipymaterialui import IconButton
from ipymaterialui import Table
from ipymaterialui import TableBody
from ipymaterialui import TableCell
from ipymaterialui import TableHead
from ipymaterialui import TableRow

from .controller import ExperimentTable
from utils import CustomText
from utils.widgets import CustomCheckbox


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

        self.header_wrapper = None
        self.body_wrapper = None
        self.body = None

        self._build_table()
        self.children = [self.header_wrapper,
                         self.body_wrapper]

    def rows(self):
        if self.body is None:
            return None
        return self.body.children

    def _build_table(self):
        head = self._build_table_head()
        body = self._build_table_body()
        self.body = body
        self.header_wrapper = Table(children=[head],
                                    size="small",
                                    style_={
                                          "width": "100%",
                                          "padding": "0px 0px",
                                      })

        table_for_body = Table(children=[body],
                               size="small",
                               style_={
                                   "width": "100%",
                                   "padding": "0px 0px 0px 0px",
                               })

        self.body_wrapper = Container(children=[table_for_body],
                                      style_={
                                            "background": "#F5F4F6",
                                            "width": "100%",
                                            # "height": "450px",
                                            "maxHeight": "585px",
                                            "overflow-y": "auto",
                                            "padding": "0px 0px 0px 0px",
                                        })

    def _build_table_head(self):
        select_cell = self._create_header_cell("", "60px")
        id_cell = self._create_header_cell("ID", "150px")
        name_cell = self._create_header_cell("Name", "150px")
        status_cell = self._create_header_cell("Status", "150px")
        description_cell = self._create_header_cell("Description", "")
        details_cell = self._create_header_cell("", "77px")

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
                                   "width": "100%",
                                   "background": "#454851",
                               })
        return table_head

    def _build_table_body(self):
        experiment_rows = []
        for row_data in self.controller.rows_data():
            row = self._create_body_row(row_data)
            experiment_rows.append(row)

        while len(experiment_rows) < 13:
            row = self._create_empty_body_row()
            experiment_rows.append(row)

        table_body = TableBody(children=experiment_rows,
                               style_={
                                   "width": "100%",
                                   "padding": "0px 0px 0px 0px",
                               })
        return table_body

    def _create_header_cell(self, text, width) -> Html:
        cell = Html(children=CustomText(text),
                    tag="th",
                    style_={

                        "text-align": "center",
                        "position": "sticky",
                        "color": "#ffffff",
                        "padding": "0px 0px 0px 0px",
                        "top": "0px",
                        "height": "45px",
                        "width": width,
                        "background": "#454851",
                        "opacity": 1.0,
                    })
        return cell

    def _create_body_row(self, experiment_data: List[str]):
        checkbox = CustomCheckbox()
        details_icon = Icon(children="open_in_new",
                            style_={
                                "font-size": "20px",
                                "padding": "0px 0px 0px 0px",
                            })
        details_button = IconButton(children=details_icon,
                                    style_={
                                        "padding": "8px 8px 8px 8px",
                                    })

        checkbox_cell = self._create_body_row_cell(checkbox, "60px", "center")
        id_cell = self._create_body_row_cell(CustomText(experiment_data[0]), "150px", "center")
        name_cell = self._create_body_row_cell(CustomText(experiment_data[1]), "150px", "left")
        status_cell = self._create_body_row_cell(CustomText(experiment_data[2]), "150px", "center")
        description_cell = self._create_body_row_cell(CustomText(experiment_data[3]), "", "left")
        details_cell = self._create_body_row_cell(details_button, "60px", "center")

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
                          self.controller.onclick_row(widget, event, data, row, checkbox))

        job_id = experiment_data[0]
        details_button.on_event("onClick",
                                lambda widget, event, data:
                                self.controller.onclick_details(widget, event, data, job_id))

        return row

    def _create_empty_body_row(self):
        checkbox_cell = self._create_body_row_cell("", "60px", "center")
        id_cell = self._create_body_row_cell("", "150px", "center")
        name_cell = self._create_body_row_cell("", "150px", "left")
        status_cell = self._create_body_row_cell("", "150px", "center")
        description_cell = self._create_body_row_cell("", "", "left")
        details_cell = self._create_body_row_cell("", "60px", "center")
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

    def _create_body_row_cell(self, children, width, align) -> TableCell:
        cell = TableCell(children=children,
                         align=align,
                         style_={
                             "padding": "0px 8px 0px 8px",
                             "width": width,
                             "height": "45px",
                         })
        return cell

