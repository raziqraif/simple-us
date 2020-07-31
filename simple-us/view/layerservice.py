from multiprocessing import cpu_count
import os
import shutil
from pathlib import Path
import threading
from typing import Optional, Tuple

import numpy
from ipyleaflet import Map, LayerGroup
from ipyleaflet import TileLayer
import osgeo
from osgeo import gdal
from osgeo.gdal import DEMProcessing
from osgeo.gdal import DEMProcessingOptions
from notebook import notebookapp

# from lib.gdal2tiles import gdal2tiles
from gdalscripts import gdal_calc
from gdalscripts import gdal2tiles
from gdalscripts import gdal_edit
from model.variableutil import VariableModel
from utils import CustomMap, SIMPLEUtil
from utils.misc import top_level_directory, NODATA
from utils.widgets.map import RasterService


class RasterLayerUtil:
    def __init__(self, variable_model: VariableModel, session_id: int):
        assert variable_model.file_path().exists()
        assert variable_model.is_raster()

        self.variable_model: VariableModel = variable_model
        self.session_id: int = session_id

        # Temporary files
        self._tif_basename = self.variable_model.file_path().stem
        self._temp_working_directory = self._get_temp_working_directory()
        self.processed_raster_path = self._temp_working_directory / (self._tif_basename + "_temp.tiff")
        self._color_file_path = self._temp_working_directory / (self._tif_basename + "_temp_color.txt")
        self._filtered_tif_path = self._temp_working_directory / (self._tif_basename + "_temp_filter.tiff")
        self._colorized_tif_path = self._temp_working_directory / (self._tif_basename + "_temp_color.tiff")
        self._remove_temp_files()  # Remove existing temp files, if exist

    def _get_temp_working_directory(self) -> Path:
        if self.variable_model.is_filtered():
            file_path = str(self.variable_model.file_path())
            id_str = self.variable_model.id_str
            file_path_root = str(SIMPLEUtil.experiment_result_path(id_str))
            suffix = file_path.split(file_path_root)[1].replace("\\", "/")
            suffix = suffix[1:] if (suffix[0] == "/") else suffix
            temp_working_directory = SIMPLEUtil.TEMP_DIR / self.variable_model.id_str / suffix
            print("temp working directory: ", temp_working_directory)
            temp_working_directory.mkdir(parents=True, exist_ok=True)
        else:
            temp_working_directory = self.variable_model.file_path().parent
        return temp_working_directory

    @property
    def _tile_folder_path(self) -> Path:
        # Cannot be accessed until self.process_raster_path is ready
        assert self.processed_raster_path.exists()

        filter_min = self.variable_model.filter_min
        filter_max = self.variable_model.filter_max
        if not self.variable_model.is_filtered():  # data is not filtered
            path = self._temp_working_directory / self._tif_basename
        else:
            min_value, max_value = self._min_max_of_raster(self.processed_raster_path)
            path = self._temp_working_directory / (self._tif_basename + "_{}_{}".format(min_value, max_value))
        return path

    @property
    def _tile_folder_url(self) -> Path:
        # Cannot be accessed until self.process_raster_path is ready
        assert self.processed_raster_path.exists()

        home = str(Path.home())
        tile_folder = str(self._tile_folder_path)
        print("tile folder:", tile_folder)
        print("tile folder split:", tile_folder.split(home))
        suffix = tile_folder.split(home)[1].replace("\\", "/")
        return SIMPLEUtil.BASE_URL + suffix + '/{z}/{x}/{-y}.png'

    def create_layer(self) -> TileLayer:
        self._process_raster()
        self._colorize_raster()
        self._tile_raster()

        # self._remove_temp_files()
        return TileLayer(url=self._tile_folder_url, opacity=0.7, name=self._tif_basename)

    def _process_raster(self):
        # Filter and warp the raster
        # self.processed_raster_path will be created

        self._filter_raster()
        # Make sure the projection is correct, and reset the NODATA value
        options = gdal.WarpOptions(dstSRS="EPSG:4326", dstNodata=NODATA, format="GTiff",
                                   resampleAlg="bilinear")
        gdal.Warp(str(self.processed_raster_path), str(self._filtered_tif_path), options=options)

    def _filter_raster(self):
        min_, max_ = self._min_max_of_raster(self.variable_model.file_path())
        range_ = max_ - min_
        new_min = min_ + self.variable_model.filter_min / float(100) * range_
        new_max = min_ + self.variable_model.filter_max / float(100) * range_

        print("filtering:")
        print("min:", min_, new_min)
        print("max:", max_, new_max)
        print("range:", range_)

        # How to use - https://gdal.org/programs/gdal_calc.html
        filter_expression = "A*logical_and(A>={},A<={})".format(new_min, new_max)
        args = ["--outfile={}".format(str(self._filtered_tif_path)),
                "-A", str(self.variable_model.file_path()),
                "--calc={}".format(filter_expression),
                "--NoDataValue=0",   # Do not change this. Explanation is in the comment below.
                "--overwrite",
                ]
        # Filter the raster data. After running this, data outside of the range will be converted to 0 and all data with
        # the value 0 will be set to NODATA. Note: It seems like the statistics metadata will not be updated properly
        # too.
        gdal_calc.run(args)

        # Remove any set statistics metadata
        gdal_edit.gdal_edit(["argv_placeholder", "-unsetstats", str(self._filtered_tif_path)])

        min_, max_ = self._min_max_of_raster(self._filtered_tif_path)
        print("finised filtering:")
        print("min:", min_)
        print("max:", max_)
        print("range:", range_)

    def _min_max_of_raster(self, tif_path: Path) -> Tuple[float, float]:
        # open the image
        raster = gdal.Open(str(tif_path))
        assert raster is not None

        # read in the crop data and get info about it
        band = raster.GetRasterBand(1)
        stats = band.GetStatistics(False, True)
        min_: float = float(stats[0])
        max_: float = float(stats[1])
        return min_, max_

    def _colorize_raster(self):
        self._create_color_file()
        options = DEMProcessingOptions(colorFilename=str(self._color_file_path), format="GTiff", addAlpha=True)
        DEMProcessing(str(self._colorized_tif_path), str(self.processed_raster_path), "color-relief", options=options)

    def _create_color_file(self):
        gtif = gdal.Open(str(self.processed_raster_path))
        srcband = gtif.GetRasterBand(1)

        # Get raster statistics
        stats = srcband.GetStatistics(False, True)
        min_ = stats[0]
        max_ = stats[1]
        file_content = "nv 0 0 0 0\n" \
                       "0% 255 0 0 255\n" \
                       "10% 255 51 0 255\n" \
                       "20% 255 119 0 255\n" \
                       "30% 255 187 0 255\n" \
                       "40% 255 255 0 255\n" \
                       "50% 204 255 0 255\n" \
                       "60% 153 255 0 255\n" \
                       "70% 102 255 0 255\n" \
                       "80% 38 191 0 255\n" \
                       "90% 0 102 0 255\n"

        if min_ == max_:
            file_content = "0% 0 102 0 255\n" \
                           "nv 0 0 0 0\n" \
                           "0 0 0 0 255\n"

        if self._color_file_path.exists():
            self._color_file_path.unlink()

        with open(str(self._color_file_path), "w+"):
            self._color_file_path.write_text(file_content)

    def _tile_raster(self):
        from utils.misc import REBUILD_RASTER_TILE
        if self._tile_folder_path.exists() and self._tile_folder_path.is_dir() and REBUILD_RASTER_TILE:
            shutil.rmtree(str(self._tile_folder_path))

        # if self.variable_model.is_filtered() and self._tile_folder_path.exists():
        #     shutil.rmtree(str(self._tile_folder_path))

        # 0 - 8 is the number of zoom level
        gdal2tiles.run(["-e", "-z", "0-8", "-a", "0, 0, 0", "--processes={}".format(cpu_count()),
                        str(self._colorized_tif_path), str(self._tile_folder_path)])

    def _remove_temp_files(self):
        # Tile folder will not be removed.
        if self._filtered_tif_path.exists():
            self._filtered_tif_path.unlink()
        if self._colorized_tif_path.exists():
            self._colorized_tif_path.unlink()
        if self._color_file_path.exists():
            self._color_file_path.unlink()


class VectorLayerUtil:
    def __init__(self, variable_model: VariableModel, session_id: int):
        assert variable_model.file_path().exists()
        assert variable_model.is_vector()

        self.variable_model: VariableModel = variable_model
        self.session_id: int = session_id

        # TODO: Finish the create layer logic

    def create_layer(self):
        return TileLayer(name=self.variable_model.file_path().stem)