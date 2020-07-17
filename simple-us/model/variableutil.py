import os
import re
from pathlib import Path
from typing import Optional, List

from utils import SIMPLEUtil

DIR_NAME_TO_DISPLAY_NAME = {"LVC": "Absolute Changes", "LVB": "Base Value", "LVA": "Updated Value",
                            "PCT": "Percent Changes"}
DISPLAY_NAME_TO_DIR_NAME = {"Absolute Changes": "LVA", "Base Value": "LVB", "Updated Value": "LVC",
                            "Percent Changes": "PCT"}


class VariableService:

    def __init__(self, experiment):
        from .experiment import Experiment
        assert isinstance(experiment, Experiment)
        self.experiment = experiment

    def _convert_variable_name(self, name: str, dir_to_display_name=True, display_to_dir_name=True) -> str:
        # NOTE: dir stands for directory
        if (name in DIR_NAME_TO_DISPLAY_NAME.keys()) and dir_to_display_name:
            name = DIR_NAME_TO_DISPLAY_NAME[name]
        elif (name in DISPLAY_NAME_TO_DIR_NAME.keys()) and display_to_dir_name:
            name = DISPLAY_NAME_TO_DIR_NAME[name]

        return name

    def directory_to_display_name(self, variable: str):
        self._convert_variable_name(variable, display_to_dir_name=False)

    def display_to_directory_name(self, variable: str):
        self._convert_variable_name(variable, dir_to_display_name=False)

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

    def _shock_dir_name(self, spatial_resolution_path: Path) -> str:
        shock_dirname = os.listdir(str(spatial_resolution_path))[0]  # LOOKATME: Assume there's only one shock directory
        return shock_dirname

    def type_of_result_options(self, system_component: str, spatial_resolution: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        options = []
        spatial_resolution_path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) \
                                  / Path(spatial_resolution)
        if not spatial_resolution_path.is_dir():
            return options
        if len(os.listdir(spatial_resolution_path)) == 0:
            return options
        # LOOKATME: Assume there's only one shock directory
        shock_dirname = self._shock_dir_name(spatial_resolution_path)

        path_ = spatial_resolution_path / Path(shock_dirname)
        if not path_.is_dir():
            return options
        for item in os.listdir(path_):
            if not path_.joinpath(item).is_dir():
                continue
            if intersected_paths is None:
                options.append(self._convert_variable_name(item))
            elif self._variables_intersected(intersected_paths, system_component, spatial_resolution, item):
                options.append(self._convert_variable_name(item))
        return options

    def _type_of_result_path(self, system_component: str, spatial_resolution: str, type_of_result: str) -> Path:
        type_of_result = self._convert_variable_name(type_of_result, dir_to_display_name=False)
        spatial_resolution_path = SIMPLEUtil.result_path(self.id_str) / Path(system_component) \
                                  / Path(spatial_resolution)
        shock_dirname = self._shock_dir_name(spatial_resolution_path)
        path_ = spatial_resolution_path / Path(shock_dirname) / Path(type_of_result)
        return path_

    def result_to_view_options(self, system_component: str, spatial_resolution: str, type_of_result: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        path_ = self._type_of_result_path(system_component, spatial_resolution, type_of_result)
        options = []
        if not path_.is_dir():
            return options
        if len(os.listdir(str(path_))) == 0:
            return options

        for full_path in path_.glob("*.tif"):
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
            converted_tor = self._convert_variable_name(type_of_result, dir_to_display_name=False)
            pattern += converted_tor + ".*"
        if spatial_resolution and type_of_result and result_to_view:
            converted_rtv = self._convert_variable_name(result_to_view, dir_to_display_name=False)
            pattern += converted_rtv

        compiled = re.compile(pattern)
        filtered = list(filter(compiled.match, intersected_paths))
        return len(filtered) != 0

    def result_path(self, system_component: Optional[str] = None, spatial_resolution: Optional[str] = None,
                    type_of_result: Optional[str] = None, result_to_view: Optional[str] = None) -> Optional[Path]:
        # Format: ../root_job_dir/<id>/<system_component>/<spatial_resolution>/<shock_dir>/<type_of_result>
        # /<result_to_view>

        # TODO: Use this method to simplify some of the above methods

        path_ = SIMPLEUtil.result_path(self.id_str)
        if system_component is None:
            return path_ if path_.exists() else None
        path_ = path_ / system_component
        if spatial_resolution is None:
            return path_ if path_.exists() else None
        path_ = path_ / spatial_resolution
        if type_of_result is None:
            return path_ if path_.exists() else None
        path_ = path_ / self._shock_dir_name(path_) / self.display_to_directory_name(type_of_result)
        if result_to_view is None:
            return path_ if path_.exists() else None
        path_ = path_ / result_to_view / self.display_to_directory_name(result_to_view)
        return path_

    def intersect_result_paths(self, experiment) -> List[str]:
        """
            Intersect all result paths for both experiments (when the root result directory is excluded) and return the
            values
        """
        from .experiment import Experiment
        assert isinstance(experiment, Experiment)

        first_root = SIMPLEUtil.result_path(self.id_str)
        second_root = SIMPLEUtil.result_path(experiment.id_str)

        first_prefix_len = len(str(first_root)) + 1
        second_prefix_len = len(str(second_root)) + 1

        first_paths = [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.tif")]
        second_paths = [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.tif")]

        intersected_paths = [path_ for path_ in first_paths if path_ in second_paths]
        return intersected_paths
