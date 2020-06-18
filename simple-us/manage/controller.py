from copy import copy

from .table import ExperimentTable
from .view import ManageTabView
from utils import ExperimentChip


class ManageTab:
    def __init__(self):
        self.experiment_table = ExperimentTable()
        self.view = ManageTabView(self, self.experiment_table.view)
        self.experiment_table.create_experiment_chip = lambda id_, name: self.view.append_chip(id_, name)
        self.experiment_table.delete_experiment_chip = lambda id_: self.view.remove_chip(id_)

    def ondelete_chip(self, widget: ExperimentChip, event, data):
        experiment_id = widget.experiment_id
        associated_row = self.experiment_table.selected_row_with_id(experiment_id)

        if associated_row:
            self.experiment_table.deselect_row(associated_row)

        chips_wrapper = self.view.chips_wrapper
        children = copy(chips_wrapper.children)
        children.remove(widget)
        chips_wrapper.children = children
