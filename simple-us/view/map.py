from pathlib import Path
from typing import Optional

from ipyleaflet import Map
import osgeo
from osgeo import gdal
from osgeo.gdal import DEMProcessing
from osgeo.gdal import DEMProcessingOptions

from utils.misc import top_level_directory

DEM_COLORS = [
    # "255 0 0",
    "0 0 0",
    "255 51 0",
    "255 119 0",
    "255 187 0",
    "255 255 0",
    "204 255 0",
    "153 255 0",
    "102 255 0",
    "38 191 0",
    "0 102 0"
]


class MapService:
    def __init__(self, map_1: Map, map_2: Optional[Map] = None):
        self.map_1 = map_1
        self.map_2 = map_2

    def _tif_type(self, tif_path: Path) -> str:
        file_name = tif_path.name
        split_1 = file_name.split("_")
        split_2 = split_1[2].split(".")
        type_ = split_2[0]
        return type_

    def create_colored_tif(self, tif_path: Path, color_file_path: Path) -> Path:
        assert tif_path.exists()
        assert color_file_path.exists()
        directory = tif_path.parent
        file_name = self._tif_type(tif_path) + "_color"
        file_path = directory / file_name
        options = DEMProcessingOptions(colorFilename=str(color_file_path), format="GTiff",
                                       computeEdges=True)
        # options = DEMProcessingOptions(format="GTiff", addAlpha=True)
        DEMProcessing(str(file_path), str(tif_path), "color-relief", options=options)
        return file_path

    def create_tile_folder(self, tif_path: Path):
        assert tif_path.exists()
        directory = tif_path.parent
        options = DEMProcessingOptions()


if __name__ == "__main__":
    svc = MapService(None, None)
    tif_ = Path("C:/Users/muhdr/SimpleUSRun/job/1/outputs/Production/Geospatial/p_QCROPgl/LVB/p_QCROPgl_irrigated.tif")
    tif_type = svc._tif_type(tif_)
    # color_file = svc._create_color_file(tif_)
    color_file = (top_level_directory() / "utils/color.txt").absolute()
    print("type:", tif_type)
    print("create color_file:", color_file)
    colored_tif = svc.create_colored_tif(tif_, color_file)
    print("create colored tiff:", colored_tif)
