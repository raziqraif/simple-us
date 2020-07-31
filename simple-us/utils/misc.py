from pathlib import Path

DEBUG_MODE = 0
PRIMARY_COLOR = "#306178"
PRIMARY_COLOR_DARK = "#2b7a78"
PRIMARY_COLOR_LIGHT = "#e35183"
BACKGROUND_COLOR_LIGHT = "#f5f5f6"
BACKGROUND_COLOR = "#e1e2e1"
INNER_BACKGROUND_COLOR = BACKGROUND_COLOR_LIGHT
MAIN_BACKGROUND_COLOR = "#ffffff"

NODATA = -999999999  # Nodata value for processed raster file.
REBUILD_RASTER_TILE = False # Existing tile folder will be deleted upon visualization if this value is set to yes.


def top_level_directory() -> Path:
    return Path(__file__).parent.parent

