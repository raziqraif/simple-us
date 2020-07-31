from typing import Any
from typing import List
from typing import Optional

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
from utils import BACKGROUND_COLOR
from utils import BACKGROUND_COLOR_LIGHT
from utils import CustomText
from utils import CustomCheckbox
from utils import INNER_BACKGROUND_COLOR
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR


class ExperimentTableView(Container):
    def __init__(self, controller: ExperimentTable):
        super(Container, self).__init__()

        self.style_ = {
            "display": "flex",
            "padding": "0px 0px 0px 0px",
            "flex-direction": "column",
        }
        self.controller = controller

        self.header_wrapper = None
        self.body_wrapper = None
        self.body = None

        self.selected_rows = []

        self._build_table()
        self.children = [self.header_wrapper,
                         self.body_wrapper]

    def _build_table(self):
        head = self._build_table_head()
        body = self._build_table_body()
        self.body = body
        table_for_head = Table(children=[head],
                               size="small",
                               style_={
                                   "padding": "0px 0px 0px 0px",
                               })
        self.header_wrapper = Container(children=[table_for_head],
                                        style_={
                                            "padding": "0px 0px 0px 0px",
                                            "display": "flex",
                                            "flex-direction": "column",
                                        })

        table_for_body = Table(children=[body],
                               size="small",
                               style_={
                                   "padding": "0px 0px 0px 0px",
                               })

        self.body_wrapper = Container(children=[table_for_body],
                                      style_={
                                            "maxHeight": "585px",
                                            "overflow-y": "auto",
                                            "padding": "0px 0px 0px 0px",
                                            "display": "flex",
                                            "flex-direction": "column",
                                            "border": "1px solid " + PRIMARY_COLOR,
                                        })

    def _build_table_head(self):
        refresh_icon = Icon(children="refresh",
                            style_={
                                "color": "white",
                                "font-size": "21px",
                                "padding": "0px 0px 0px 0px",
                            })
        refresh_button = IconButton(children=refresh_icon,
                                    style_={
                                        "width": "35px",
                                        "height": "35px",
                                        "padding": "0px 0px 0px 0px",
                                    })
        select_cell = self._create_header_cell("", "60px")
        id_cell = self._create_header_cell("ID", "150px")
        name_cell = self._create_header_cell("Name", "180px")
        status_cell = self._create_header_cell("Status", "150px")
        description_cell = self._create_header_cell("Description", "235px")
        details_cell = self._create_header_cell("", "77px", padding="0px 16px 0px 0px")
        extra_cell = self._create_header_cell(refresh_button, "77px", padding="0px 16px 0px 0px")

        header_cells = [select_cell,
                        id_cell,
                        name_cell,
                        status_cell,
                        description_cell,
                        details_cell]

        header_row = TableRow(children=header_cells,
                              style_={
                                  "padding": "0px 8px 0px 32px",
                              })
        table_head = TableHead(children=[header_row],
                               sticky_header=True,
                               style_={
                                   "background": PRIMARY_COLOR,
                               })
        return table_head

    def _create_header_cell(self, text, width, padding="0px 0px 0px 0px") -> Html:
        cell = Html(children=CustomText(text),
                    tag="th",
                    style_={

                        "text-align": "center",
                        "position": "sticky",
                        "color": "#ffffff",
                        "padding": padding,
                        "top": "0px",
                        "height": "45px",
                        "width": width,
                        "opacity": 1.0,
                    })
        return cell

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
                                   "padding": "0px 0px 0px 0px",
                                   "background": "white",
                               })
        return table_body

    def _create_body_row(self, experiment_data: List[str]):
        checkbox = CustomCheckbox()
        details_icon = Icon(children="open_in_new",
                            style_={
                                "font-size": "20px",
                                "padding": "0px 0px 0px 0px",
                            })
        details_button = IconButton(children=details_icon,
                                    style_={
                                        "width": "35px",
                                        "height": "35px",
                                        "padding": "0px 0px 0px 0px",
                                    })

        checkbox_cell = self._create_body_row_cell(checkbox, 60, "center")
        id_cell = self._create_body_row_cell(experiment_data[0], 150, "center")
        name_cell = self._create_body_row_cell(experiment_data[1], 180, "left")
        status_cell = self._create_body_row_cell(experiment_data[2], 150, "center")
        description_cell = self._create_body_row_cell(experiment_data[3], 235, "left")
        details_cell = self._create_body_row_cell(details_button, 60, "center")

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

        # Register event to all cells but details_cell, as it will affect details_button as well
        for cell in cells[:-1]:
            cell.on_event("onClick",
                          lambda widget, event, data:
                          self.controller.onclick_row(widget, event, data, row))

        job_id = experiment_data[0]
        details_button.on_event("onClick",
                                lambda widget, event, data:
                                self.controller.onclick_details(widget, event, data, job_id))
        return row

    def _create_empty_body_row(self):
        checkbox_cell = self._create_body_row_cell("", 0, "center")
        id_cell = self._create_body_row_cell("", 0, "center")
        name_cell = self._create_body_row_cell("", 0, "left")
        status_cell = self._create_body_row_cell("", 0, "center")
        description_cell = self._create_body_row_cell("", 0, "left")
        details_cell = self._create_body_row_cell("", 0, "center")
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

    def _create_body_row_cell(self,
                              children: Any,
                              width: int,
                              align: str) -> TableCell:

        text_width = width
        if isinstance(children, str):
            children = CustomText(children,
                                  style_={
                                      "text-overflow": "ellipsis",
                                      "width": "{}px".format(text_width),
                                      "maxWidth": "{}px".format(text_width),
                                      "overflow": "hidden",
                                      "padding": "0px 0px 0px 0px",
                                      "white-space": "nowrap"
                                  }, tag="div")

        cell = TableCell(children=children,
                         align=align,
                         style_={
                             "padding": "0px 4px 0px 4px",
                             "width": "{}px".format(width),
                             "height": "45px",
                         })

        return cell

    def _select_row(self, row: TableRow) -> None:
        checkbox = self.checkbox_from_row(row)
        checkbox.checked = True
        row.selected = True

    def _deselect_row(self, row: TableRow) -> None:
        checkbox = self.checkbox_from_row(row)
        checkbox.checked = False
        row.selected = False

    def rows(self):
        if self.body is None:
            return None
        return self.body.children

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

    def selected_row_from_id(self, experiment_id: str) -> Optional[TableRow]:
        experiment_id = experiment_id.strip()
        for row in self.selected_rows:
            id_in_row = self.id_from_row(row)
            if id_in_row == experiment_id:
                return row
        return None

    def selected_experiment_ids(self) -> List[str]:
        ids = []
        for row in self.selected_rows:
            id_ = self.id_from_row(row)
            ids.append(id_)
        return ids

    def toggle_row(self, row: TableRow):
        checkbox = self.checkbox_from_row(row)
        if not checkbox.checked:
            if len(self.selected_rows) >= 2:
                # TODO: Replace this with a snickbar.
                return
            else:
                self._select_row(row)
                self.selected_rows.append(row)
                name = self.name_from_row(row)
                id_ = self.id_from_row(row)
                self.controller.create_experiment_chip(id_, name)
        elif checkbox.checked:
            self._deselect_row(row)
            self.selected_rows.remove(row)
            id_ = self.id_from_row(row)
            self.controller.delete_experiment_chip(id_)
