from pathlib import Path

DEBUG_MODE = 0
# PRIMARY_COLOR = "#294866"
PRIMARY_COLOR = "#2F5275"
SECONDARY_COLOR = "#f73378"
BACKGROUND_COLOR = "#e1e2e1"
BUTTON_COLOR = "#1DA1F2"
INNER_BACKGROUND_COLOR = "#f5f5f6"
MAIN_BACKGROUND_COLOR = "#ffffff"
GREEN = "#35B535"
GREEN = "#35B535"

NODATA = -999999999  # Nodata value for processed raster file.
REBUILD_RASTER_TILE = False  # Existing tile folder will be deleted upon visualization if this value is set to yes.


def top_level_directory() -> Path:
    return Path(__file__).parent.parent

