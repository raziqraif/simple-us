import os
from os import listdir
import re
from pathlib import Path
from typing import Optional, List

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

    def shock_dirname(self) -> str:
        shock_dirname = VariableService.shock(self.id_str, self.system_component(), self.spatial_resolution())
        return shock_dirname

    def file_path(self) -> Path:
        return VariableService.result_to_view_path(self.id_str, self.system_component(), self.spatial_resolution(),
                                                   self.type_of_result(), self.result_to_view())

    def processed_tif_path(self) -> Path:
        # Not necessarily already existed
        assert self.type_of_result(as_dirname=True).lower() == "geospatial"
        path_ = self.file_path().parent
        file_name = self.file_path().stem + "_temp.tiff"
        return path_ / file_name

    def colorized_tif_path(self) -> Path:
        # Not necessarily already existed
        # Only for tif file visualization
        assert self.type_of_result(as_dirname=True).lower() == "geospatial"
        path_ = self.file_path().parent
        file_name = self.file_path().stem + "_temp_color.tiff"
        return path_ / file_name

    def tile_folder_path(self) -> Path:
        # Only for tif file visualization
        assert self.type_of_result(as_dirname=True).lower() == "geospatial"
        path_ = self.file_path().parent
        if (self.filter_min == 0) and (self.filter_max == 100):
            folder_name = self.file_path().stem + "_{}_{}".format(self.filter_min, self.filter_max)
        else:
            folder_name = self.file_path().stem + "_filtered"

        return path_ / folder_name

    def remove_temp_files(self):
        self.processed_tif_path().unlink(missing_ok=True)
        self.colorized_tif_path().unlink(missing_ok=True)


class VariableService:
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
        shock_name = cls.shock(id_str, system_component, spatial_resolution)
        file_format = ".tif" if spatial_resolution.lower() == "geospatial" else ".shp"
        suffix = cls._result_to_view_suffix(result_to_view)
        name = None
        if to_directory_name:
            name = "{}_{}{}".format(shock_name, suffix, file_format) if len(suffix) != 0 \
                else "{}{}".format(shock_name, file_format)
        elif to_display_name:
            name = cls._result_to_view_display_name(result_to_view, id_str, system_component, spatial_resolution,
                                                    type_of_result)
        assert name is not None
        return name

    @classmethod
    def _result_to_view_display_name(cls, result_to_view: str, id_str: str, system_component: str,
                                     spatial_resolution: str, type_of_result: str) -> str:
        assert id_str is not None       # Not used, as of current display name format
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
    def system_component_options(cls, id_str: str, intersected_paths: Optional[List[str]] = None) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        root = SIMPLEUtil.result_path(id_str)
        options = []
        if not root.is_dir():
            return options
        for system_component in os.listdir(root):
            if not root.joinpath(system_component).is_dir():
                continue
            if (intersected_paths is None) or cls._variables_intersect(intersected_paths, id_str, system_component):
                converted = cls.convert_system_component(system_component, to_display_name=True)
                options.append(converted)
        return options

    @classmethod
    def spatial_resolution_options(cls, id_str: str, system_component: str,
                                   intersected_paths: Optional[List[str]] = None) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        system_component_path = cls.system_component_path(id_str, system_component)
        options = []
        if not system_component_path.is_dir():
            return options
        for spatial_resolution in os.listdir(system_component_path):
            if not system_component_path.joinpath(spatial_resolution).is_dir():
                continue
            if (intersected_paths is None) or cls._variables_intersect(intersected_paths, system_component,
                                                                       spatial_resolution):
                converted = cls.convert_spatial_resolution(spatial_resolution, to_display_name=True)
                options.append(converted)
        return options

    @classmethod
    def type_of_result_options(cls, id_str: str, system_component: str, spatial_resolution: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        options = []
        path_ = cls.shock_path(id_str, system_component, spatial_resolution)
        if not path_.is_dir():
            return options
        for item in os.listdir(str(path_)):
            if not path_.joinpath(item).is_dir():
                continue
            if (intersected_paths is None) or cls._variables_intersect(intersected_paths, system_component,
                                                                       spatial_resolution, item):
                converted = cls.convert_type_of_result(item, to_display_name=True)
                options.append(converted)
        return options

    @classmethod
    def result_to_view_options(cls, id_str: str, system_component: str, spatial_resolution: str, type_of_result: str,
                               intersected_paths: Optional[List[str]] = None) -> List[str]:
        # Note: The variables need to be in one of the intersected paths if intersected_paths is specified
        type_of_result_path = cls.type_of_result_path(id_str, system_component, spatial_resolution, type_of_result)
        options = []
        if not type_of_result_path.is_dir():
            return options
        if len(os.listdir(str(type_of_result_path))) == 0:
            return options

        pattern = "*.tif" if spatial_resolution.lower() == "geospatial" else "*.shp"
        for full_path in type_of_result_path.glob(pattern):
            if not type_of_result_path.joinpath(full_path).is_file():
                continue
            if (intersected_paths is None) or cls._variables_intersect(intersected_paths, id_str, system_component,
                                                                       spatial_resolution, full_path.name):
                converted = cls.convert_result_to_view(full_path.name, id_str, system_component, spatial_resolution,
                                                       type_of_result, to_display_name=True)
                options.append(converted)
        return options

    @classmethod
    def _variables_intersect(cls, intersected_paths: List[str], id_str: str, system_component: str,
                             spatial_resolution: Optional[str] = None, type_of_result: Optional[str] = None,
                             result_to_view: Optional[str] = None) -> bool:

        pattern = cls.convert_system_component(system_component, to_directory_name=True) + ".*"
        if spatial_resolution:
            pattern += spatial_resolution + ".*"
        if spatial_resolution and type_of_result:
            converted_tor = cls.convert_type_of_result(type_of_result, to_directory_name=True)
            pattern += converted_tor + ".*"
        if spatial_resolution and type_of_result and result_to_view:
            converted_rtv = cls.convert_result_to_view(result_to_view, id_str, system_component, spatial_resolution,
                                                       type_of_result, to_directory_name=True)
            pattern += converted_rtv

        compiled = re.compile(pattern)
        filtered = list(filter(compiled.match, intersected_paths))
        return len(filtered) != 0

    @classmethod
    def system_component_path(cls, id_str, system_component: str):
        path_ = SIMPLEUtil.result_path(id_str) / cls.convert_system_component(system_component, to_directory_name=True)
        return path_

    @classmethod
    def spatial_resolution_path(cls, id_str: str, system_component: str, spatial_resolution: str) -> Path:
        path_ = cls.system_component_path(id_str, system_component) \
                / cls.convert_spatial_resolution(spatial_resolution, to_directory_name=True)
        return path_

    @classmethod
    def shock(cls, id_str: str, system_component: str, spatial_resolution: str) -> str:
        spatial_resolution_path = cls.spatial_resolution_path(id_str, system_component, spatial_resolution)
        directories = listdir(str(spatial_resolution_path))
        shock_dirname = directories[0]  # LOOKATME: Assume there's only one shock directory
        return shock_dirname

    @classmethod
    def shock_path(cls, id_str: str, system_component: str, spatial_resolution: str) -> Path:
        spatial_resolution_path = cls.spatial_resolution_path(id_str, system_component, spatial_resolution)
        # Assumption: There is only one shock directory
        shock_dirname = cls.shock(id_str, system_component, spatial_resolution)
        return spatial_resolution_path / shock_dirname

    @classmethod
    def type_of_result_path(cls, id_str: str, system_component: str, spatial_resolution: str,
                            type_of_result: str) -> Path:

        path_ = cls.shock_path(id_str, system_component, spatial_resolution) / cls.convert_type_of_result(
            type_of_result, to_directory_name=True)
        return path_

    @classmethod
    def result_to_view_path(cls, id_str: str, system_component: str, spatial_resolution: str,
                            type_of_result: str, result_to_view: str) -> Path:

        path_ = cls.type_of_result_path(id_str, system_component, spatial_resolution, type_of_result) \
                / cls.convert_result_to_view(result_to_view, id_str, system_component, spatial_resolution,
                                             type_of_result, to_directory_name=True)
        return path_

    @classmethod
    def intersect_variable_paths(cls, first_id_str: str, second_id_str: str) -> List[str]:
        """
            Intersect all full variable paths from both experiments (aka, intersect all result-to-view paths from both
            experiments) when the root result directory is excluded and return the values
        """

        first_root = SIMPLEUtil.result_path(first_id_str)
        second_root = SIMPLEUtil.result_path(second_id_str)

        first_prefix_len = len(str(first_root)) + 1
        second_prefix_len = len(str(second_root)) + 1

        first_paths = [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.tif")]
        first_paths += [str(path_)[first_prefix_len:] for path_ in first_root.glob("**/*.shp")]
        second_paths = [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.tif")]
        second_paths += [str(path_)[second_prefix_len:] for path_ in second_root.glob("**/*.shp")]

        intersected_paths = [path_ for path_ in first_paths if path_ in second_paths]
        return intersected_paths
