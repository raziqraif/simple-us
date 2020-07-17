import os
import shutil
from pathlib import Path
from typing import Optional

from ipyleaflet import Map
from ipyleaflet import TileLayer
import osgeo
from osgeo import gdal
from osgeo.gdal import DEMProcessing
from osgeo.gdal import DEMProcessingOptions
from notebook import notebookapp

from lib.gdal2tiles import GDAL2Tiles
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
    def __init__(self):
        pass

    def _tif_type(self, tif_path: Path) -> str:
        file_name = tif_path.name
        split_1 = file_name.split("_")
        if len(split_1) >= 3:
            split_2 = split_1[2].split(".")
            type_ = split_2[0]
        else:
            type_ = "temp_type"
        return type_

    def create_color_file(self, tif_path: Path) -> Path:
        gtif = gdal.Open(str(tif_path))
        srcband = gtif.GetRasterBand(1)

        # Get raster statistics
        stats = srcband.GetStatistics(True, True)
        min_ = stats[0]
        max_ = stats[1]
        print("min:", min_)
        print("max:", max_)
        file_content = "0% 255 0 0\n" \
                       "10% 255 51 0\n" \
                       "20% 255 119 0\n" \
                       "30% 255 187 0\n" \
                       "40% 255 255 0\n" \
                       "50% 204 255 0\n" \
                       "60% 153 255 0\n" \
                       "70% 102 255 0\n" \
                       "80% 38 191 0\n" \
                       "90% 0 102 0\n" \
                       "nv 0 0 0\n" \
                       "0 0 0 0\n"

        if min_ == max_:
            file_content = "0% 0 102 0\n" \
                           "nv 0 0 0\n" \
                           "0 0 0 0\n"

        dir_ = tif_path.parent
        type_ = self._tif_type(tif_path)
        file_name = type_ + "_color.txt"
        file_path = dir_ / file_name
        with open(str(file_path), "w+") as fp:
            file_path.write_text(file_content)
        return file_path

    def create_colored_tif(self, tif_path: Path, color_file_path: Path) -> Path:
        assert tif_path.exists()
        assert color_file_path.exists()
        directory = tif_path.parent
        file_name = self._tif_type(tif_path) + "_color.tiff"
        file_path = directory / file_name
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
        options = DEMProcessingOptions(colorFilename=str(color_file_path), format="GTiff",
                                       computeEdges=True)
        # options = DEMProcessingOptions(format="GTiff", addAlpha=True)
        DEMProcessing(str(file_path), str(tif_path), "color-relief", options=options)
        return file_path

    def create_tile_folder(self, tif_path: Path):
        assert tif_path.exists()
        directory = tif_path.parent
        file_name = tif_path.stem
        tile_dirname = file_name + "_tiles"
        tile_dirpath = directory / tile_dirname
        if tile_dirpath.exists() and tile_dirpath.is_dir():
            shutil.rmtree(str(tile_dirpath))
        # tool = GDAL2Tiles(["-e", "-z", "3-6", "-a", "0,0,0", str(tif_path), str(tile_dirpath)])
        tool = GDAL2Tiles(["-z", "4-6", "-a", "0,0,0", str(tif_path), str(tile_dirpath)])
        tool.process()
        return tile_dirpath

    def add_layer(self, map_: Map, tif_path: Path):
        assert tif_path.exists()
        # color_path = (top_level_directory() / "utils/color.txt").absolute()
        color_path = self.create_color_file(tif_path)
        print("color path:", color_path)
        color_tif = self.create_colored_tif(tif_path, color_path)
        tile_path = self.create_tile_folder(color_tif)
        base_url = self._base_url()
        print("base url :", base_url)
        str_tile_path_wo_home = str(tile_path).split(str(Path.home()))[1].replace("\\", "/")
        print("tile path w/o home:", str_tile_path_wo_home)
        url = base_url + str_tile_path_wo_home + '/{z}/{x}/{-y}.png'
        print("url:", url)
        layer = TileLayer(url=url, opacity=.5, name="layer")
        # map_.clear_layers()
        map_.add_layer(layer)

    def _base_url(self) -> str:
        if ("HOSTNAME" in os.environ.keys()) and ("mygeohub" in os.environ["HOSTNAME"]):
            # From geotiff tutorial code
            base_url = "https://proxy.mygeohub.org"
            nb = None
            session = os.environ['SESSION']
            servers = list(notebookapp.list_running_servers())
            for server in servers:
                if session in server['base_url']:
                    nb = server['base_url']
                    nb_dir = server['notebook_dir']
                    print("nb", nb)
                    print("nb_dir", nb_dir)
                    break
            base_url += nb + "tree"
        else:
            base_url = "http://localhost:8888/tree"
        return base_url


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
    tile_dir = svc.create_tile_folder(colored_tif)
    print(tile_dir)
