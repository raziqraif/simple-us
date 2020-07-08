import re
import os
from pathlib import Path
from typing import Optional, List

from utils import SIMPLEUtil

DIR_NAME_TO_DISPLAY_NAME = {"LVC": "Absolute Changes", "LVB": "Base Value", "LVA": "Updated Value",
                            "PCT": "Percent Changes"}
DISPLAY_NAME_TO_DIR_NAME = {"Absolute Changes": "LVA", "Base Value": "LVB", "Updated Value": "LVC",
                            "Percent Changes": "PCT"}


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

    def _convert_variable_name(self, name: str, dir_to_display=True, display_to_dir=True) -> str:
        if (name in DIR_NAME_TO_DISPLAY_NAME.keys()) and dir_to_display:
            name = DIR_NAME_TO_DISPLAY_NAME[name]
        elif (name in DISPLAY_NAME_TO_DIR_NAME.keys()) and display_to_dir:
            name = DISPLAY_NAME_TO_DIR_NAME[name]
        return name

    def system_component_options(self, intersected_paths: Optional[List[str]] = None) -> List[str]:
        path_ = SIMPLEUtil.result_path(self.id_str)
        options = []
        if not path_.is_dir():
            return options
        for item in os.listdir(path_):
            if not path_.joinpath(item).is_dir():
                continue
            if intersected_paths is None:
                options.append(item)
            elif self._variables_intersected(intersected_paths, item):
                options.append(item)
        return options

    def spatial_resolution_options(self, system_component: str, intersected_paths: Optional[List[str]] = None) \
            -> List[str]:
        path_ = SIMPLEUtil.result_path(self.id_str) / Path(system_component)
        options = []
        if not path_.is_dir():
            return options
        for item in os.listdir(path_):
            if not path_.joinpath(item).is_dir():
                continue
            if intersected_paths is None:
                options.append(item)
            elif self._variables_intersected(intersected_paths, system_component, item):
                options.append(item)
        return options

    def type_of_result_options(self, system_component: str, spatial_resolution: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        options = []
        spatial_resolution_path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) \
            / Path(spatial_resolution)
        if not spatial_resolution_path.is_dir():
            return options
        if len(os.listdir(spatial_resolution_path)) == 0:
            return options
        shock_dirname = os.listdir(spatial_resolution_path)[0]  # LOOKATME: Assume there's only one shock directory

        path_ = spatial_resolution_path / Path(shock_dirname)
        if not path_.is_dir():
            return options
        for item in os.listdir(path_):
            if not path_.joinpath(item).is_dir():
                continue
            if intersected_paths is None:
                options.append(item)
            elif self._variables_intersected(intersected_paths, system_component, spatial_resolution, item):
                options.append(item)
        return options

    def result_to_view_options(self, system_component: str, spatial_resolution: str, type_of_result: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        type_of_result_path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) / Path(spatial_resolution) \
               / Path(self._convert_variable_name(type_of_result))

        options = []
        if not type_of_result_path.is_dir():
            return options
        if len(os.listdir(type_of_result_path)) == 0:
            return options
        middle_dir_name = os.listdir(type_of_result_path)[0]  # TODO: Check this with older version
        path_ = type_of_result_path / Path(middle_dir_name)
        if not path_.is_dir():
            return options
        for full_path in path_.glob("*.tif^"):
            if not path_.joinpath(full_path).is_file():
                continue
            if intersected_paths is None:
                options.append(full_path.name)
            elif self._variables_intersected(intersected_paths, system_component, spatial_resolution, full_path.name):
                options.append(full_path.name)

        return options

    def _variables_intersected(self, intersected_paths: List[str], system_component: str,
                               spatial_resolution: Optional[str] = None, type_of_result: Optional[str] = None,
                               result_to_view: Optional[str] = None) -> bool:

        pattern = system_component + ".*"
        if spatial_resolution:
            pattern += spatial_resolution + ".*"
        if spatial_resolution and type_of_result:
            converted_tor = self._convert_variable_name(type_of_result, dir_to_display=False)
            pattern += converted_tor + ".*"
        if spatial_resolution and type_of_result and result_to_view:
            converted_rtv = self._convert_variable_name(result_to_view, dir_to_display=False)
            pattern += converted_rtv

        print("pattern:", pattern)
        compiled = re.compile(pattern)
        filtered = list(filter(compiled.match, intersected_paths))
        return len(filtered) != 0

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

    def intersect_result_paths(self, experiment) -> List[str]:
        """
            Intersect all result paths for both experiments (when the root result directory is excluded) and return the
            values
        """

        assert isinstance(experiment, Experiment)

        first_root = SIMPLEUtil.result_path(self.id_str)
        second_root = SIMPLEUtil.result_path(experiment.id_str)

        first_prefix_len = len(str(first_root)) + 1
        second_prefix_len = len(str(second_root)) + 1

        first_paths = [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.tif")]
        second_paths = [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.tif")]

        intersected_paths = [path_ for path_ in first_paths if path_ in second_paths]
        return intersected_paths


if __name__ == "__main__":
    e1 = Experiment(1)
    e2 = Experiment(2)
    ip = e1.intersect_result_paths(e2)
    for path in ip:
        print(path)
    print(e1._variables_intersected(ip, "Production", "Geospatial", "Absolute Changes", "rainfed.tif"))
