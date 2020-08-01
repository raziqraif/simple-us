import os
from os import listdir
from os.path import splitext
import re
from pathlib import Path
from typing import Optional, List, Set, Union

from utils import SIMPLEUtil

TYPE_OF_RESULT_TO_DISPLAY = {"LVC": "Absolute Changes", "LVB": "Base Value", "LVA": "Updated Value",
                             "PCT": "Percent Changes"}
TYPE_OF_RESULT_TO_DIRNAME = {"Absolute Changes": "LVC", "Base Value": "LVB", "Updated Value": "LVA",
                             "Percent Changes": "PCT"}


class VariableModel:
    def __init__(self, id_str: str, system_component: str, spatial_resolution: str, type_of_result: str,
                 result_to_view: str, filter_min: int, filter_max: int):
        assert 0 <= filter_min <= filter_max <= 100
        self.id_str = id_str
        self._system_component: str = VariableService.convert_system_component(system_component, to_display_name=True)
        self._spatial_resolution: str = VariableService.convert_spatial_resolution(spatial_resolution,
                                                                                   to_display_name=True)
        self._type_of_result: str = VariableService.convert_type_of_result(type_of_result, to_display_name=True)
        self._result_to_view: str = VariableService.convert_result_to_view(result_to_view, self.id_str,
                                                                           self.system_component(),
                                                                           self.spatial_resolution(),
                                                                           self.type_of_result(), to_display_name=True)
        self.filter_min: int = filter_min
        self.filter_max: int = filter_max

    def system_component(self, as_dirname=False) -> str:
        value = self._system_component
        if as_dirname:
            value = VariableService.convert_system_component(value, to_directory_name=True)
        return value

    def spatial_resolution(self, as_dirname=False) -> str:
        value = self._spatial_resolution
        if as_dirname:
            value = VariableService.convert_spatial_resolution(value, to_directory_name=True)
        return value

    def type_of_result(self, as_dirname=False) -> str:
        value = self._type_of_result
        if as_dirname:
            value = VariableService.convert_type_of_result(value, to_directory_name=True)
        return value

    def result_to_view(self, as_filename=False) -> str:
        value = self._result_to_view
        if as_filename:
            value = VariableService.convert_result_to_view(value, self.id_str, self.system_component(),
                                                           self.spatial_resolution(), self.type_of_result(),
                                                           to_directory_name=True)
        return value

    def simple_variable(self) -> str:
        simple_variable = VariableService.simple_variable(self.id_str, self.system_component(),
                                                          self.spatial_resolution())
        return simple_variable

    def file_path(self) -> Path:
        # NOTE: Variable path format - .../system component/spatial resolution/SIMPLE variable/type of result/result to
        # view

        return VariableService.result_to_view_path(self.id_str, self.system_component(), self.spatial_resolution(),
                                                   self.type_of_result(), self.result_to_view())

    def is_raster(self):
        extension = splitext(str(self.file_path()))[1]
        return ".tif" in extension  # Can be .tiff too

    def is_vector(self):
        return not self.is_raster()

    def is_filtered(self):
        return not ((self.filter_min == 0) and (self.filter_max == 100))


class VariableService:
    # Variable path format - SIMPLEUtil.result_path(id_str) / system component/spatial resolution/SIMPLE variable \
    # /type of result/result to view

    def __init__(self, id_str_1: str, id_str_2: Optional[str] = None):
        self.id_str_1: str = id_str_1
        self.id_str_2: str = id_str_2

        # The options for each variable is stored in a set
        self._system_components: Set = set()
        self._spatial_resolutions: dict = {}  # spatial_resolution as key
        self._simple_variables: dict = {}  # (system_component, spatial_resolution) as key
        # NOTE: It is assumed that there is only one simple variable for each pair of system component and spatial
        # resolution. So, simple_variable is not used as a key for _type_of_results
        self._type_of_results: dict = {}  # (system_component, spatial_resolution) as key
        self._results_to_view: dict = {}  # (system_component, spatial_resolution, type_of_result) as key

        self._read_variables()

    def _read_variables(self):
        variable_paths = self._get_variable_paths()
        for path in variable_paths:
            self._process_variable_path(path)

    def _process_variable_path(self, truncated_variable_path: str):
        path = truncated_variable_path.replace("\\", "/")
        path = path if path[0] != "/" else path[1:]
        variables = path.split("/")
        system_component, spatial_resolution, simple_variable, type_of_result, result_to_view = variables
        display_system_component = self.convert_system_component(system_component, to_display_name=True)
        display_spatial_resolution = self.convert_spatial_resolution(spatial_resolution, to_display_name=True)
        display_type_of_result = self.convert_type_of_result(type_of_result, to_display_name=True)
        display_result_to_view = self.convert_result_to_view(result_to_view, self.id_str_1,  system_component,
                                                             spatial_resolution, type_of_result, to_display_name=True)
        self._system_components.add(display_system_component)
        if system_component in self._spatial_resolutions.keys():
            self._spatial_resolutions[system_component].add(display_spatial_resolution)
        else:
            self._spatial_resolutions[system_component] = {display_spatial_resolution}
        if (system_component, spatial_resolution) in self._simple_variables.keys():
            self._simple_variables[(system_component, spatial_resolution)].add(simple_variable)
        else:
            self._simple_variables[(system_component, spatial_resolution)] = {simple_variable}
        # NOTE: It is assumed that there is only one simple variable for each pair of system component and spatial
        # resolution. So, simple_variable is not used as a key for _type_of_results
        if (system_component, spatial_resolution) in self._type_of_results.keys():
            self._type_of_results[(system_component, spatial_resolution)].add(display_type_of_result)
        else:
            self._type_of_results[(system_component, spatial_resolution)] = {display_type_of_result}
        if (system_component, spatial_resolution, type_of_result) in self._results_to_view.keys():
            self._results_to_view[(system_component, spatial_resolution, type_of_result)].add(display_result_to_view)
        else:
            self._results_to_view[(system_component, spatial_resolution, type_of_result)] = {display_result_to_view}

    def _get_variable_paths(self) -> List[str]:
        # Note: SIMPLEUtil.result_path(id_str) will be truncated from the paths
        # Note: If id_str_2 is specified, the paths will be intersected.
        first_root = SIMPLEUtil.experiment_result_path(self.id_str_1)
        first_prefix_len = len(str(first_root)) + 1  # +1 to account for the forward/back slash
        first_paths = [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.tif")]
        first_paths += [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.shp")]

        if self.id_str_2:
            second_root = SIMPLEUtil.experiment_result_path(self.id_str_2)
            second_prefix_len = len(str(second_root)) + 1
            second_paths = [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.tif")]
            second_paths += [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.shp")]

            valid_paths = [path_ for path_ in first_paths if path_ in second_paths]
        else:
            valid_paths = first_paths
        return valid_paths

    def has_valid_variables(self) -> bool:
        return len(self.system_component_options()) != 0

    def system_component_options(self) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        options = list(self._system_components)
        options.sort()
        return options

    def spatial_resolution_options(self, system_component: str) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        system_component = self.convert_system_component(system_component, to_directory_name=True)
        options = list(self._spatial_resolutions[system_component])
        options.sort()
        return options

    def type_of_result_options(self, system_component: str, spatial_resolution: str) -> List[str]:
        system_component = self.convert_system_component(system_component, to_directory_name=True)
        spatial_resolution = self.convert_spatial_resolution(spatial_resolution, to_directory_name=True)
        options = list(self._type_of_results[(system_component, spatial_resolution)])
        options.sort()
        return options

    def result_to_view_options(self, system_component: str, spatial_resolution: str, type_of_result: str) -> List[str]:
        system_component = self.convert_system_component(system_component, to_directory_name=True)
        spatial_resolution = self.convert_spatial_resolution(spatial_resolution, to_directory_name=True)
        type_of_result = self.convert_type_of_result(type_of_result, to_directory_name=True)
        options = list(self._results_to_view[(system_component, spatial_resolution, type_of_result)])
        options.sort()
        return options

    @classmethod
    def convert_system_component(cls, system_component: str, to_display_name=False, to_directory_name=False):
        # Convert from display name to directory name or vice versa
        assert to_directory_name or to_display_name
        return system_component  # No changes, as of current version

    @classmethod
    def convert_spatial_resolution(cls, spatial_resolution: str, to_display_name=False, to_directory_name=False):
        # Convert from display name to directory name or vice versa
        assert to_directory_name or to_display_name
        return spatial_resolution  # No changes, as of current version

    @classmethod
    def convert_type_of_result(cls, type_of_result: str, to_display_name=False, to_directory_name=False):
        # Convert from display name to directory name or vice versa
        assert to_directory_name or to_display_name
        if (type_of_result in TYPE_OF_RESULT_TO_DISPLAY.keys()) and to_display_name:
            type_of_result = TYPE_OF_RESULT_TO_DISPLAY[type_of_result]
        elif (type_of_result in TYPE_OF_RESULT_TO_DIRNAME.keys()) and to_directory_name:
            type_of_result = TYPE_OF_RESULT_TO_DIRNAME[type_of_result]
        return type_of_result

    @classmethod
    def convert_result_to_view(cls, result_to_view: str, id_str: str, system_component: str, spatial_resolution: str,
                               type_of_result: str, to_display_name=False, to_directory_name=False):
        # Convert from display name to directory name or vice versa
        assert to_directory_name or to_display_name
        spatial_resolution_path = cls.spatial_resolution_path(id_str, system_component, spatial_resolution)
        simple_variable = listdir(str(spatial_resolution_path))[0]  # It is assumed there is only one simple variable
        # directory
        file_format = ".tif" if spatial_resolution.lower() == "geospatial" else ".shp"
        suffix = cls._result_to_view_suffix(result_to_view)
        name = None
        if to_directory_name:
            name = "{}_{}{}".format(simple_variable, suffix, file_format) if len(suffix) != 0 \
                else "{}{}".format(simple_variable, file_format)
        elif to_display_name:
            name = cls._result_to_view_display_name(result_to_view, id_str, system_component, spatial_resolution,
                                                    type_of_result)
        assert name is not None
        return name

    @classmethod
    def _result_to_view_display_name(cls, result_to_view: str, id_str: str, system_component: str,
                                     spatial_resolution: str, type_of_result: str) -> str:
        assert id_str is not None  # Not used, as of current display name format
        assert type_of_result is not None
        system_component = cls.convert_system_component(system_component, to_display_name=True).lower()
        spatial_resolution = cls.convert_spatial_resolution(spatial_resolution, to_display_name=True).lower()
        name = system_component
        if system_component == "production":
            name = "Output"
        elif system_component == "water":
            name = "Water Use"
        elif system_component == "environment":
            name = "N Use"
        elif system_component == "land":
            name = "Land Use"

        if spatial_resolution == "geospatial":
            name += " - Grid"
        elif spatial_resolution == "regional":
            name += " - Region"
        elif spatial_resolution == "global":
            name += " - Global"

        suffix = cls._result_to_view_suffix(result_to_view)
        if len(suffix) != 0:
            name += ", {}".format(suffix)
        return name

    @classmethod
    def _result_to_view_suffix(cls, result_to_view: str) -> str:
        # ASSUMPTION: Suffix is displayed on both dirname and display name for result_to_view
        result_to_view = result_to_view.lower()
        suffix = ""
        if "irrigated" in result_to_view:
            suffix = "irrigated"
        elif "rainfed" in result_to_view:
            suffix = "rainfed"
        return suffix

    @classmethod
    def system_component_path(cls, id_str, system_component: str):
        path_ = SIMPLEUtil.experiment_result_path(id_str) / cls.convert_system_component(system_component,
                                                                                         to_directory_name=True)
        return path_

    @classmethod
    def spatial_resolution_path(cls, id_str: str, system_component: str, spatial_resolution: str) -> Path:
        path_ = cls.system_component_path(id_str, system_component) \
                / cls.convert_spatial_resolution(spatial_resolution, to_directory_name=True)
        return path_

    @classmethod
    def simple_variable(cls, id_str: str, system_component: str, spatial_resolution: str) -> str:
        spatial_resolution_path = cls.spatial_resolution_path(id_str, system_component, spatial_resolution)
        directories = listdir(str(spatial_resolution_path))
        simple_variable = directories[0]  # LOOKATME: Assume there's only one simple variable directory
        return simple_variable

    @classmethod
    def simple_variable_path(cls, id_str: str, system_component: str, spatial_resolution: str) -> Path:
        spatial_resolution_path = cls.spatial_resolution_path(id_str, system_component, spatial_resolution)
        # Assumption: There is only one simple variable directory
        simple_variable = cls.simple_variable(id_str, system_component, spatial_resolution)
        return spatial_resolution_path / simple_variable

    @classmethod
    def type_of_result_path(cls, id_str: str, system_component: str, spatial_resolution: str,
                            type_of_result: str) -> Path:

        path_ = cls.simple_variable_path(id_str, system_component, spatial_resolution) / cls.convert_type_of_result(
            type_of_result, to_directory_name=True)
        return path_

    @classmethod
    def result_to_view_path(cls, id_str: str, system_component: str, spatial_resolution: str,
                            type_of_result: str, result_to_view: str) -> Path:

        path_ = cls.type_of_result_path(id_str, system_component, spatial_resolution, type_of_result) \
                / cls.convert_result_to_view(result_to_view, id_str, system_component, spatial_resolution,
                                             type_of_result, to_directory_name=True)
        return path_
