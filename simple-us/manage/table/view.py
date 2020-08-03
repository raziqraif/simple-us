from copy import copy
from typing import Any, Callable
from typing import List
from typing import Optional

from ipymaterialui import Container, Button
from ipymaterialui import Html
from ipymaterialui import Icon
from ipymaterialui import IconButton
from ipymaterialui import Table
from ipymaterialui import TableBody
from ipymaterialui import TableCell
from ipymaterialui import TableHead
from ipymaterialui import TableRow

from model import Experiment
from .controller import ExperimentTable
from utils import BACKGROUND_COLOR
from utils import CustomText
from utils import CustomCheckbox
from utils import INNER_BACKGROUND_COLOR
from utils import MAIN_BACKGROUND_COLOR
from utils import PRIMARY_COLOR


# Cell width macros
CHECKBOX_WIDTH = 70
ID_WIDTH = 150
NAME_WIDTH = 180
STATUS_WIDTH = 150
AUTHOR_WIDTH = 150
DESCRIPTION_WIDTH = 295
# Keys to sort the table
ID_SORTKEY = "ID"
NAME_SORTKEY = "NAME"
STATUS_SORTKEY = "STATUS"
AUTHOR_SORTKEY = "AUTHOR"
DESCRIPTION_SORTKEY = "DESCRIPTION"


class TableRowWithExperiment(TableRow):
    def __init__(self, experiment: Optional[Experiment],  **kwargs):
        super().__init__(**kwargs)
        self.experiment = experiment


class ExperimentTableView(Container):
    def __init__(self, controller: ExperimentTable):
        super(Container, self).__init__()

        self.style_ = {
            "display": "flex",
            "margin": "0px 0px 0px 0px",
            "padding": "0px 0px 0px 0px",
            "flex-direction": "column",
        }
        self.controller = controller

        self._header_wrapper = None
        self._body_wrapper = None
        self._rows_wrapper = None  # Rows will be stored here

        self._sort_by = ID_SORTKEY
        self._sort_increasingly = True  # This will get toggled every time _sort_by was changed

        self.selected_rows: List[TableRowWithExperiment] = []

        self._initialize_widgets()
        self.children = [self._header_wrapper,
                         self._body_wrapper]

    def _initialize_widgets(self):
        head = self._create_table_head()
        self._build_rows_wrapper()
        table_for_head = Table(children=[head],
                               size="small",
                               style_={
                                   "margin": "0px 0px 0px 0px",
                                   "padding": "0px 0px 0px 0px",
                                   "table-layout": "fixed",
                               })
        self._header_wrapper = Container(children=[table_for_head],
                                         style_={
                                            "margin": "0px 0px 0px 0px",
                                            "padding": "0px 0px 0px 0px",
                                            "display": "flex",
                                            "flex-direction": "column",
                                        })

        table_for_body = Table(children=[self._rows_wrapper],
                               size="small",
                               style_={
                                   "margin": "0px 0px 0px 0px",
                                   "padding": "0px 0px 0px 0px",
                                   "table-layout": "fixed",
                               })

        self._body_wrapper = Container(children=[table_for_body],
                                       style_={
                                            "maxHeight": "585px",
                                            "overflow-y": "auto",
                                            "margin": "0px 0px 0px 0px",
                                            "padding": "0px 0px 0px 0px",
                                            "display": "flex",
                                            "flex-direction": "column",
                                            "border": "1px solid " + PRIMARY_COLOR,
                                        })

    def _create_table_head(self):
        select_cell = self._create_header_cell("", CHECKBOX_WIDTH)
        id_cell = self._create_header_cell("ID", ID_WIDTH)
        name_cell = self._create_header_cell("Name", NAME_WIDTH)
        status_cell = self._create_header_cell("Status", STATUS_WIDTH)
        author_cell = self._create_header_cell("Author", AUTHOR_WIDTH)
        description_cell = self._create_header_cell("Description", DESCRIPTION_WIDTH)
        details_cell = self._create_header_cell("", None)

        header_cells = [select_cell,
                        id_cell,
                        name_cell,
                        status_cell,
                        author_cell,
                        description_cell,
                        details_cell]

        header_row = TableRow(children=header_cells,
                              style_={
                                  "margin": "0px 0px 0px 0px",
                                  "padding": "0px 8px 0px 32px",
                              })
        table_head = TableHead(children=[header_row],
                               sticky_header=True,
                               style_={
                                   "background": PRIMARY_COLOR,
                               })
        self._register_header_buttons(id_cell.children, name_cell.children, status_cell.children, author_cell.children,
                                      description_cell.children)
        return table_head

    def _register_header_buttons(self, id_button: Button, name_button: Button, status_button: Button,
                                 author_button: Button, description_button: Button):
        id_button.on_event("onClick", lambda widget, event, data: self.sort_table(ID_SORTKEY))
        name_button.on_event("onClick", lambda widget, event, data: self.sort_table(NAME_SORTKEY))
        status_button.on_event("onClick", lambda widget, event, data: self.sort_table(STATUS_SORTKEY))
        author_button.on_event("onClick", lambda widget, event, data: self.sort_table(AUTHOR_SORTKEY))
        description_button.on_event("onClick", lambda widget, event, data: self.sort_table(DESCRIPTION_SORTKEY))

    def _create_header_cell(self, text: str, width: Optional[int]) -> TableCell:
        html_text = CustomText(text,
                               style_={
                                   "width": "{}px".format(width),
                                   "maxWidth": "{}px".format(width),
                                   "color": "white",
                                   "font-size": "12px",
                               })
        button = Button(children=html_text,
                        center_ripple=True,
                        style_={
                            "width": "{}px".format(width),
                            "height": "100%",
                            "padding": "0px 0px 0px 0px",
                            "margin": "0px 0px 0px 0px",
                            "background": PRIMARY_COLOR,
                        })
        children = html_text if len(text) == 0 else button
        cell = TableCell(children=children,
                         align="center",
                         style_={
                             "text-align": "center",
                             "position": "sticky",
                             "color": "#ffffff",
                             "padding": "0px 0px 0px 0px",
                             "margin": "0px 0px 0px 0px",
                             "top": "0px",
                             "height": "45px",
                             "width": "{}px".format(width),
                             "opacity": 1.0,
                         })
        return cell

    def _build_rows_wrapper(self):
        self._rows_wrapper = TableBody(children=[],
                                       style_={
                                           "margin": "0px 0px 0px 0px",
                                           "padding": "0px 0px 0px 0px",
                                           "background": "white",
                                           "table-layout": "fixed",
                              })
        self.refresh_table()

    def _create_body_row(self, experiment: Experiment):
        checkbox = CustomCheckbox()
        details_icon = Icon(children="open_in_new",
                            style_={
                                "font-size": "20px",
                                "margin": "0px 0px 0px 0px",
                                "padding": "0px 0px 0px 0px",
                            })
        details_button = IconButton(children=details_icon,
                                    style_={
                                        "width": "35px",
                                        "height": "35px",
                                        "margin": "0px 0px 0px 0px",
                                        "padding": "0px 0px 0px 0px",
                                    })

        checkbox_cell = self._create_body_row_cell(checkbox, CHECKBOX_WIDTH, "center")
        id_cell = self._create_body_row_cell(experiment.id_str, ID_WIDTH, "center")
        name_cell = self._create_body_row_cell(experiment.name_str, NAME_WIDTH, "center")
        status_cell = self._create_body_row_cell(experiment.status_str, STATUS_WIDTH, "center")
        author_cell = self._create_body_row_cell(experiment.author_str, AUTHOR_WIDTH, "center")
        description_cell = self._create_body_row_cell(experiment.description_str, DESCRIPTION_WIDTH, "left")
        details_cell = self._create_body_row_cell(details_button, None, "center")

        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            author_cell,
            description_cell,
            details_cell
        ]

        row = TableRowWithExperiment(experiment=experiment,
                                     children=cells,
                                     style_={
                                         "margin": "0px 0px 0px 0px",
                                         "padding": "0px 0px 0px 0px",
                                     },
                                     hover=True, selected=False, ripple=True)

        # Register event to all cells but details_cell, as it will affect details_button as well
        for cell in cells[:-1]:
            cell.on_event("onClick",
                          lambda widget, event, data:
                          self.controller.onclick_row(widget, event, data, row))

        job_id_str = experiment.id_str
        details_button.on_event("onClick",
                                lambda widget, event, data:
                                self.controller.onclick_details(widget, event, data, job_id_str))
        return row

    def _create_empty_body_row(self):
        checkbox_cell = self._create_body_row_cell("", 0, "center")
        id_cell = self._create_body_row_cell("", 0, "center")
        name_cell = self._create_body_row_cell("", 0, "left")
        status_cell = self._create_body_row_cell("", 0, "center")
        author_cell = self._create_body_row_cell("", 0, "center")
        description_cell = self._create_body_row_cell("", 0, "left")
        details_cell = self._create_body_row_cell("", 0, "center")
        cells = [
            checkbox_cell,
            id_cell,
            name_cell,
            status_cell,
            author_cell,
            description_cell,
            details_cell
        ]
        row = TableRowWithExperiment(experiment=None,
                                     children=cells,
                                     style_={
                                         "margin": "0px 0px 0px 0px",
                                         "padding": "0px 0px 0px 0px",
                                     },
                                     hover=False, selected=False, ripple=True)
        return row

    def _create_body_row_cell(self,
                              children: Any,
                              width: Optional[int],
                              align: str) -> TableCell:

        if isinstance(children, str):
            text_width = width - 16 if width is not None else None
            children = CustomText(children,
                                  style_={
                                      "text-overflow": "ellipsis",
                                      "width": "{}px".format(text_width),
                                      "maxWidth": "{}px".format(text_width),
                                      "overflow": "hidden",
                                      "margin": "0px 8px 0px 8px",
                                      "padding": "0px 0px 0px 0px",
                                      "white-space": "nowrap"
                                  }, tag="div")

        cell = TableCell(children=children,
                         align=align,
                         style_={
                             "padding": "0px 0px 0px 0px",
                             "margin": "0px 0px 0px 0px",
                             "width": "{}px".format(width),
                             "height": "45px",
                             # "display": "flex",
                             # "flex-direction": "column",
                             # "align-items": align,
                             # "justify-content": "center",
                         })

        return cell

    def _select_row(self, row: TableRowWithExperiment) -> None:
        checkbox = self._checkbox_from_row(row)
        checkbox.checked = True
        row.selected = True

    def _deselect_row(self, row: TableRowWithExperiment) -> None:
        checkbox = self._checkbox_from_row(row)
        checkbox.checked = False
        row.selected = False

    def _checkbox_from_row(self, row: TableRowWithExperiment) -> CustomCheckbox:
        checkbox_cell = row.children[0]
        checkbox = checkbox_cell.children
        return checkbox

    def _id_str_from_row(self, row: TableRowWithExperiment) -> str:
        id_cell = row.children[1]
        id_div = id_cell.children
        id = id_div.children
        return id.strip()

    def _name_from_row(self, row: TableRowWithExperiment) -> str:
        name_cell = row.children[2]
        name_div = name_cell.children
        name = name_div.children
        return name.strip()

    def _status_from_row(self, row: TableRowWithExperiment) -> str:
        status_cell = row.children[3]
        status_div = status_cell.children
        status = status_div.children
        return status.strip()

    def _author_from_row(self, row: TableRowWithExperiment) -> str:
        status_cell = row.children[4]
        status_div = status_cell.children
        status = status_div.children
        return status.strip()

    def _description_from_row(self, row: TableRowWithExperiment) -> str:
        status_cell = row.children[4]
        status_div = status_cell.children
        status = status_div.children
        return status.strip()

    def selected_row_from_id_str(self, experiment_id_str: str) -> Optional[TableRowWithExperiment]:
        experiment_id_str = experiment_id_str.strip()
        for row in self.selected_rows:
            id_in_row = self._id_str_from_row(row)
            if id_in_row == experiment_id_str:
                return row
        return None

    def selected_experiments_id_strs(self) -> List[str]:
        ids = []
        for row in self.selected_rows:
            id_ = self._id_str_from_row(row)
            ids.append(id_)
        return ids

    def toggle_row(self, row: TableRowWithExperiment):
        checkbox = self._checkbox_from_row(row)
        if not checkbox.checked:
            if len(self.selected_rows) >= 2:
                # TODO: Replace this with a snickbar.
                return
            else:
                self._select_row(row)
                self.selected_rows.append(row)
                name = self._name_from_row(row)
                id_ = self._id_str_from_row(row)
                self.controller.create_experiment_chip(id_, name)
        elif checkbox.checked:
            self._deselect_row(row)
            self.selected_rows.remove(row)
            id_ = self._id_str_from_row(row)
            self.controller.delete_experiment_chip(id_)

    def refresh_table(self):
        experiments = self.controller.load_experiments()
        experiment_rows = self._make_rows_from_experiments(experiments)

        self.deselect_selected_rows()
        self._rows_wrapper.children = experiment_rows
        self.sort_table(ID_SORTKEY, toggle_order=False)

    def _make_rows_from_experiments(self, experiments: List[Experiment]) -> List[TableRowWithExperiment]:
        experiment_rows = []
        for experiment in experiments:
            row = self._create_body_row(experiment)
            experiment_rows.append(row)
        # TODO: Remove this test data
        while len(experiment_rows) < 13:
            row = self._create_empty_body_row()
            experiment_rows.append(row)
        return experiment_rows

    def deselect_selected_rows(self):
        while len(self.selected_rows) > 0:
            self.toggle_row(self.selected_rows[0])

    def sort_table(self, sort_by: str = None, toggle_order=True, default=False):
        if default:
            self._sort_by = ID_SORTKEY
            self._sort_increasingly = True
        elif sort_by is not None:
            if (sort_by == self._sort_by) and toggle_order:
                self._sort_increasingly = not self._sort_increasingly
            else:
                self._sort_increasingly = True
            self._sort_by = sort_by

        rows = copy(self._rows_wrapper.children)
        non_empty_rows = [row for row in rows if isinstance(row.children[0].children, CustomCheckbox)]
        empty_rows = [row for row in rows if not isinstance(row.children[0].children, CustomCheckbox)]
        reverse = not self._sort_increasingly

        if self._sort_by == ID_SORTKEY:
            private_rows = [row for row in non_empty_rows if Experiment.is_private_id_str(self._id_str_from_row(row))]
            shared_rows = [row for row in non_empty_rows if Experiment.is_shared_id_str(self._id_str_from_row(row))]
            private_rows.sort(key=lambda row: Experiment.to_id(self._id_str_from_row(row)), reverse=reverse)
            shared_rows.sort(key=lambda row: Experiment.to_id(self._id_str_from_row(row)), reverse=reverse)
            non_empty_rows = [*private_rows, *shared_rows]
        elif self._sort_by == NAME_SORTKEY:
            non_empty_rows.sort(key=lambda row: self._name_from_row(row), reverse=reverse)
        elif self._sort_by == STATUS_SORTKEY:
            non_empty_rows.sort(key=lambda row: self._status_from_row(row), reverse=reverse)
        elif self._sort_by == AUTHOR_SORTKEY:
            non_empty_rows.sort(key=lambda row: self._author_from_row(row), reverse=reverse)
        elif self._sort_by == DESCRIPTION_SORTKEY:
            non_empty_rows.sort(key=lambda row: self._description_from_row(row), reverse=reverse)
        self._rows_wrapper.children = non_empty_rows + empty_rows
