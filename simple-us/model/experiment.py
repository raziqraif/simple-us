import os
from pathlib import Path
from typing import Optional, List

from utils import SIMPLEUtil


class ExperimentUtil:
    @staticmethod
    def to_id(id_str: str) -> int:
        # TODO: Update this
        return int(id_str)

    @staticmethod
    def to_id_str(id_: int, is_private=True) -> str:
        # TODO: Update this
        return str(id_)

    @staticmethod
    def is_private_id_str(id_str) -> bool:
        return True  # TODO: Update this

    @staticmethod
    def is_shared_id_str(id_str) -> bool:
        return False  # TODO: Update this

    @staticmethod
    def from_id_str(id_str: str):
        id_ = Experiment.to_id(id_str)
        is_private = Experiment.is_private_id_str(id_str)
        print("id, private =", id_, is_private)
        exp = Experiment.from_id(id_, is_private)
        return exp

    @staticmethod
    def from_id(id_: int, is_private: bool):
        from database import DBManager
        db = DBManager(private_experiments=is_private)
        exp = db.get_experiment(id_)
        return exp


class Experiment(ExperimentUtil):
    """ Class to represent the SIMPLEJobs db table

    Values are stored as they are read from the the db. Helper functions are used if the values
    need to be transformed.
    """

    def __init__(self,
                 id: int = -1,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 description: Optional[str] = None,
                 model: Optional[str] = None,
                 submission_id: Optional[str] = None,
                 submission_time: Optional[str] = None,
                 published: Optional[int] = None,
                 author: Optional[str] = None,
                 ):
        self.id = id
        self.name = name
        self.status = status
        self.model = model
        self.description = description
        self.author = author
        self.submission_id = submission_id
        self.submission_time = submission_time
        self.published = published

    """ General property methods """

    @property
    def id_str(self) -> str:
        return Experiment.to_id_str(self.id)

    @property
    def name_str(self) -> str:
        return self.name if self.name is not None else ""

    @property
    def status_str(self) -> str:
        return self.status if self.status is not None else ""

    @property
    def model_str(self) -> str:
        return self.model if self.model is not None else ""

    @property
    def description_str(self) -> str:
        return self.description if self.description is not None else ""

    @property
    def author_str(self) -> str:
        return self.author if self.author is not None else ""

    @property
    def submission_id_str(self) -> str:
        return self.submission_id if self.submission_id is not None else ""

    @property
    def submission_time_str(self) -> str:
        return self.submission_time if self.submission_time is not None else ""

    @property
    def published_str(self) -> str:
        # TODO: Needs to return "SHARED" or "PUBLIC"
        return str(self.submission_time) if self.submission_time is not None else ""

    @property
    def is_private(self):
        return Experiment.is_private_id_str(self.id_str)

    @property
    def is_completed(self):
        return self.status_str.lower() == "completed"

    """ Methods to access result variables """

    def system_component_options(self) -> List[str]:
        path = SIMPLEUtil.result_path(self.id_str)
        options = []
        if not path.is_dir():
            return options
        options += [item for item in os.listdir(path) if path.joinpath(item).is_dir()]
        return options

    def spatial_resolution_options(self, system_component: str) -> List[str]:
        path = SIMPLEUtil.result_path(self.id_str) / Path(system_component)
        options = []
        if not path.is_dir():
            return options
        options += [item for item in os.listdir(path) if path.joinpath(item).is_dir()]
        return options

    def type_of_result_options(self, system_component: str, spatial_resolution: str) -> List[str]:
        path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) / Path(spatial_resolution)
        conversion = {"LVA": "Absolute Changes", "LVB": "Base Value", "LVC": "Updated Value",
                      "PVT": "Percent Changes"}

        options = []
        if not path.is_dir():
            return options
        options += [conversion[item] for item in os.listdir(path) if path.joinpath(item).is_dir()]
        return options

    def result_to_view_options(self, system_component: str, spatial_resolution: str,
                               type_of_result: str) -> List[str]:
        type_of_result_path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) / Path(spatial_resolution) \
               / Path(type_of_result)

        options = []
        if not type_of_result_path.is_dir():
            return options
        if len(os.listdir(type_of_result_path)) == 0:
            return options
        middle_dir_name = os.listdir(type_of_result_path)[0]  # TODO: Check this with older version
        path = type_of_result_path / Path(middle_dir_name)

        options += [item for item in path.glob("*.tif")]
        return options

    @property
    def variable_options(self) -> dict:
        variables = {}
        system_components = self.system_component_options()

        for i in system_components:
            variables[i] = {}
            spatial_resolutions = self.spatial_resolution_options(i)
            for j in spatial_resolutions:
                variables[i][j] = {}
                type_of_results = self.type_of_result_options(i, j)
                for k in type_of_results:
                    variables[i][j][k] = self.result_to_view_options(i, j, k)

        return variables

    def intersect_variable_options(self, variable_options: dict):
        first = self.variable_options
        second = variable_options

        variables = {}
        for i in first.keys():
            if i in second.keys():
                variables[i] = {}
            for j in first[i].keys():
                if j in second[i].keys():
                    variables[i][j] = {}
                for k in first[i][j].keys():
                    if k in second[i][j].keys():
                        list_ = [item for item in first[i][j][k] if item in second[i][j][k]]
                        variables[i][j][k] = list_

        return variables

    def _validate_variable_options(self, variables: dict):
        for i in variables.keys():
            if len(variables[i]) == 0:
                variables.pop(i)
                if len(variables) == 0:
                    return variables
                continue
            for j in variables[i].keys():
                if len(variables[i][j]) == 0:
                    variables[i].pop(j)
                    if len(variables[i]) == 0:
                        return variables
                    continue
            # TODO Finish this
            #     for
            # Check if variables[i] is empty


if __name__ == "__main__":
    Experiment()
