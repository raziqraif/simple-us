import os
from pathlib import Path
import time
import threading
from typing import List
from typing import Optional

from ipymaterialui import Popover, Popper, Container
from IPython.core.display import display
from ipyleaflet import DrawControl, TileLayer
from ipyleaflet import FullScreenControl
from ipyleaflet import LayersControl
from ipyleaflet import Map
from ipyleaflet import ScaleControl
from ipyleaflet import SearchControl
from ipyleaflet import WidgetControl
from ipyleaflet import ZoomControl
from ipywidgets import Output, VBox, jslink
from ipywidgets import Layout
from osgeo import gdal

from model.variableutil import VariableModel


class CustomMap(Map):
    def __init__(self, width: str, height: str):
        from .text import CustomText
        super().__init__(scroll_wheel_zoom=True, zoom_control=False)
        self.layout = Layout(width=width, height=height, margin="8px 0px 0px 0px")
        self.center = (39.5, -98.35)
        self.zoom = 4

        self._legend_bar = LegendBar()
        self._gdal_layer: Optional[TileLayer] = None  # Can be a raster layer or a vector layer.
        self._raster_service: Optional[RasterService] = None
        self._variable_model = None
        self._linked_map: Optional[CustomMap] = None

        self._coordinates_text = CustomText("Coordinates: -", style_={"font-size": '11px'})
        self._value_text = CustomText("Value: -", style_={"font-size": '11px'})
        self._value_area = VBox(children=[self._coordinates_text, self._value_text],
                                layout=Layout(min_width="174px", height="42px", padding="4px 4px 4px 4px"))

        self.add_control(WidgetControl(widget=self._legend_bar, position="bottomleft"))
        self.add_control(ZoomControl(position="topleft"))
        self.add_control(FullScreenControl(position="topleft"))
        self.add_control(DrawControl(position='topleft', circlemarker={}, polyline={}))
        self.add_control(LayersControl(position="topright"))
        self.add_control(WidgetControl(widget=self._value_area, position="bottomright"))
        self.on_interaction(self._mouse_event)

    def link(self, map_):
        assert isinstance(map_, self.__class__)
        jslink((self, "zoom"), (map_, "zoom"))
        jslink((self, "center"), (map_, "center"))
        self._linked_map = map_

    def visualize_vector(self, layer: TileLayer):
        # TODO: Implement this
        if self._gdal_layer:
            self.substitute_layer(self._gdal_layer, layer)
        else:
            self.add_layer(layer)
        self._gdal_layer = layer
        self._raster_service = None
        self._legend_bar.refresh(None, None)
        self.center = (39.5, -98.35)
        self.zoom = 4

    def visualize_raster(self, layer: TileLayer, raster_path: Path):
        """ The raster path should have been processed and filtered, if needed. """

        self._raster_service = RasterService(raster_path)
        if self._gdal_layer:
            self.substitute_layer(self._gdal_layer, layer)
        else:
            self.add_layer(layer)
        self._gdal_layer = layer
        self._legend_bar.refresh(self._raster_service.min_value, self._raster_service.max_value)
        self.center = (39.5, -98.35)
        self.zoom = 4

    def _mouse_event(self, **kwargs):
        coordinates = kwargs.get('coordinates')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        self._update_value(latitude, longitude)
        if self._linked_map:
            self._linked_map._update_value(latitude, longitude)

    def _update_value(self, latitude: float, longitude: float):
        coordinates_text = 'Coordinates:  ({:.4f},{:.4f})'.format(latitude, longitude)
        if self._raster_service is None:
            value_text = "Value: -"
        else:
            value = self._raster_service.value(latitude, longitude)
            value_text = "Value: -" if value is None else "Value: {}".format(value)

        self._coordinates_text.children = coordinates_text
        self._value_text.children = value_text


class RasterService:
    def __init__(self, raster_path: Path):
        self._path = raster_path
        self._data = None

        driver = gdal.GetDriverByName('GTiff')
        dataset = gdal.Open(str(self._path))
        band = dataset.GetRasterBand(1)

        stats = band.GetStatistics(False, True)
        self.min_value: float = float(stats[0])
        self.max_value: float = float(stats[1])

        transform = dataset.GetGeoTransform()
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        self._pixel_width = float(transform[1])
        self._pixel_height = -float(transform[5])
        self._x_origin = float(transform[0])
        self._y_origin = float(transform[3])
        self._x_end = self._x_origin + self._pixel_width * cols
        self._y_end = self._y_origin - self._pixel_height * rows

        self._data = band.ReadAsArray(0, 0, cols, rows)
        dataset = None  # Close the dataset - https://gdal.org/tutorials/raster_api_tut.html

    def value(self, latitude: float, longitude: float) -> Optional[float]:
        from ..misc import NODATA
        if (longitude < self._x_origin) or (longitude > self._x_end):
            return None
        elif (latitude > self._y_origin) or (latitude < self._y_end):
            return None

        col = int((longitude - self._x_origin) / self._pixel_width)
        row = int((self._y_origin - latitude) / self._pixel_height)
        value = self._data[row][col]
        return value if value > NODATA else None


class LegendBar(Container):

    def __init__(self):
        super().__init__()
        self._bucket_width = 44
        self.style_ = self._create_style(hidden=True)

        # color for each bucket from 0% to 90%
        self.colors: List[str] = [self._rgb_to_hex(255, 0, 0),
                                  self._rgb_to_hex(255, 51, 0),
                                  self._rgb_to_hex(255, 119, 0),
                                  self._rgb_to_hex(255, 187, 0),
                                  self._rgb_to_hex(255, 255, 0),
                                  self._rgb_to_hex(204, 255, 0),
                                  self._rgb_to_hex(153, 255, 0),
                                  self._rgb_to_hex(102, 255, 0),
                                  self._rgb_to_hex(38, 191, 0),
                                  self._rgb_to_hex(0, 102, 0),
                                  ]
        self.refresh(None, None)

    def _create_style(self, bucket_number=10, hidden=False):
        style_ = {
            "width": str(self._bucket_width * bucket_number) + "px",
            "height": "15px",
            "border-radius": "15px",
            "display": "none" if hidden else "flex",
            "flex-direction": "row",
            "align-items": "center",
            "justify-content": "flex-start",
            "padding": "0px 0px 0px 0px",
        }
        return style_

    def refresh(self, min_: Optional[float], max_: Optional[float]):
        if (min_ is None) or (max_ is None):
            # Possible when every value in raster is nodata(?)
            self.style_ = self._create_style(hidden=True)
            return
        buckets = []
        if min_ == max_:
            bucket = self._create_bucket(min_, self.colors[-1])
            buckets.append(bucket)
        else:
            increment = float(max_ - min_) / len(self.colors)
            for i in range(0, len(self.colors)):
                current_value = min_ + i * increment
                bucket = self._create_bucket(current_value, self.colors[i])
                buckets.append(bucket)
        self.children = buckets
        self.style_ = self._create_style(bucket_number=len(buckets), hidden=False)

    def _create_bucket(self, value: float, color: str):
        from .text import CustomText
        if value > 1000 or value < -1000:
            value_str = "{:.2e}".format(value)
        else:
            value_str = "{:.2f}".format(value)
        text = CustomText(value_str, style_={"font-size": "8px", "opacity": "1.0"})
        bucket = Container(children=text,
                           style_={
                               "width": str(self._bucket_width) + "px",
                               "height": "20px",
                               "display": "flex",
                               "flex-direction": "row",
                               "align-items": "center",
                               "justify-content": "center",
                               "background": color,
                               "padding": "0px 0px 0px 0px",
                               "opacity": "0.75",
                           })
        return bucket

    def _rgb_to_hex(self, r: int, g: int, b: int):
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255
        return "#{:02x}{:02x}{:02x}".format(r,g,b)

