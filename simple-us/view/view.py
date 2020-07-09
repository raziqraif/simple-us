from copy import copy, deepcopy
from typing import List
from typing import Optional

from ipyleaflet import Map
from ipymaterialui import Button, Tabs, Tab
from ipymaterialui import Container
from ipymaterialui import FormControl
from ipymaterialui import FormControlLabel
from ipymaterialui import Html
from ipymaterialui import Input
from ipymaterialui import InputLabel
from ipymaterialui import MenuItem
from ipymaterialui import Select
from ipymaterialui import TextField
from ipymaterialui import TextareaAutosize
import ipywidgets as widgets
from ipywidgets import Layout

from .controller import ViewTab
from .sidebar import SidebarView
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR


class TabWithModel(Tab):
    def __init__(self, tab_model: any = None, **kwargs):
        super().__init__(**kwargs)
        self.tab_model: any = tab_model


class ViewTabUI(Container):

    def __init__(self, controller: ViewTab, sidebar: any, **kwargs):
        super().__init__(**kwargs)

        self.controller: ViewTab = controller

        self._tab_bar: Optional[Container] = None
        self._sidebar: any = sidebar
        self._maps_area: Optional[Container] = None
        self._main_area: Optional[Container] = None
        self._view_widgets_wrapper: Optional[Container] = None

        self._map_title_full: Optional[CustomText]
        self._map_title_top: Optional[CustomText] = None
        self._map_title_bottom: Optional[CustomText] = None
        self._map_wrapper_full: Optional[Container] = None
        self._map_wrapper_top: Optional[Container] = None
        self._map_wrapper_bottom: Optional[Container] = None

        self._default_tab: Optional[TabWithModel] = None
        self._empty_text: CustomText = \
            CustomText("Experiments selected for display/compare will appear here.")
        self._init_ui()

    def _init_ui(self):
        self.style_ = {
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "flex-start",
            "align-items": "center",
            "align-self": "center",
            "padding": "0px 0px 0px 0px",
            "width": "90%",
            "border": "1px solid " + PRIMARY_COLOR,
            "height": "730px",
            "margin": "40px 40px 40px 40px",
            # "border-radius": "8px",
            # "background": INNER_BACKGROUND_COLOR,
        }
        self._build_tab_bar()
        self._build_maps_area()
        self._view_widgets_wrapper = Container(children=[self._sidebar, self._maps_area],
                                               style_={
                                                  "display": "flex",
                                                  "flex-direction": "row",
                                                  "justify-content": "center",
                                                  "align-items": "center",
                                                  "align-self": "center",
                                                  "padding": "0px 0px 0px 0px",
                                                  "margin": "0px 0px 0px 0px",
                                                  # "height": "100%",
                                              })
        self._main_area = Container(children=[self._empty_text],
                                    style_={
                                       "display": "flex",
                                       "flex-direction": "column",
                                       "justify-content": "center",
                                       "align-items": "center",
                                       "align-self": "center",
                                       "padding": "0px 0px 0px 0px",
                                       "margin": "0px 0px 0px 0px",
                                       "height": "100%",
                                       "width": "100%",
                                   })
        self.children = [self._tab_bar, self._main_area]

    def _build_tab_bar(self):
        self._default_tab = CustomText("", tag="span", style_={"font-weight": "bold"})
        self._tab_bar = Tabs(
            children=[self._default_tab],
            style_={
                "background": PRIMARY_COLOR,
                # "height": "65px",
                "padding": "0px 0px 0px 0px",
                "width": "100%",
                "display": "flex",
                "flex-direction": "row",
                "align-items": "center",
            },
            centered=False, tab_model=self.controller.active_tab_model
        )

    def _build_maps_area(self):
        self._map_title_full = CustomText("", style_={"font-weight": "bold",
                                                      "font-size": "14px",
                                                      "margin": "0px 0px 8px 1px",
                                                      "align-self": "flex-start",
                                                      })
        self._map_title_top = CustomText("", style_={"font-weight": "bold",
                                                     "font-size": "14px",
                                                     "margin": "0px 0px 8px 1px",
                                                     "align-self": "flex-start",
                                                     })
        self._map_title_bottom = CustomText("", style_={"font-weight": "bold",
                                                        "font-size": "14px",
                                                        "margin": "0px 0px 8px 1px",
                                                        "align-self": "flex-start",
                                                        })
        self._map_wrapper_full = self._create_map_wrapper(self._map_title_full)
        self._map_wrapper_top = self._create_map_wrapper(self._map_title_top, False)
        self._map_wrapper_bottom = self._create_map_wrapper(self._map_title_bottom, False)
        initial_maps_area = Container(children=["test"],  # FIXME
                                      style_={
                                          "display": "flex",
                                          "flex-direction": "column",
                                          "justify-content": "center",
                                          "align-items": "center",
                                          "align-self": "center",
                                          "padding": "0px 0px 0px 0px",
                                          "margin": "0px 0px 0px 0px",
                                          "width": "650px",
                                          "height": "600px",
                                          # "width": "100%",
                                          # "height": "480px",
                                      })
        self._maps_area = initial_maps_area

    def _create_map_wrapper(self, title, full_height=True) -> Container:
        height = "100%" if full_height else "50%"
        wrapper = Container(children=[title],
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": "center",
                                # "width": "618px",
                                "height": height,
                                "padding": "1px 1px 1px 1px",
                                "margin": "0px 0px 0px 24px",
                            })
        return wrapper

    def _create_empty_map(self, full_height=True):
        height = "570px" if full_height else "270px"
        layout = Layout(width="600px", height=height)
        return Map(layout=layout, center=(39.5, -98.35), zoom=4)  # TODO: Update this

    def new_tab(self, tab_name: str, tab_model: any, comparison: bool = False):
        children = self._tab_bar.children
        children = copy(children) if children[0] != self._default_tab else []  # copy() is needed.
        # It seems like if the memory address of children is the same, the DOM will not get updated.

        tab = TabWithModel(label=CustomText(tab_name,
                                            style_={
                                                "color": "#ffffff",
                                                "padding": "0px 0px 0px 0px",
                                            }), tab_model=tab_model, selected=True)
        children.append(tab)
        self._tab_bar.children = children
        self._tab_bar.value = tab
        if comparison:
            maps = [self._create_empty_map(full_height=False) for count in range(2)]
        else:
            maps = [self._create_empty_map()]
        self.controller.save_maps_to_model(maps, tab_model)
        self._show_map(tab_model)

    def _show_map(self, tab_model: any):
        maps = self.controller.maps_from_model(tab_model)
        assert 1 <= len(maps) <= 2
        if len(maps) == 1:
            self._show_full_map(tab_model)
        elif len(maps) == 2:
            self._show_comparison_maps(tab_model)

    def _show_full_map(self, tab_model: any):
        if self._main_area.children[0] == self._empty_text:
            self._main_area.children = [self._view_widgets_wrapper]
        title = self.controller.map_titles_from_model(tab_model)[0]
        map_ = self.controller.maps_from_model(tab_model)[0]

        self._map_title_full.children = title
        self._map_wrapper_full.children = [self._map_title_full, map_]
        self._maps_area.children = [self._map_wrapper_full]

    def _show_comparison_maps(self, tab_model: any):
        if self._main_area.children[0] == self._empty_text:
            self._main_area.children = [self._view_widgets_wrapper]
        titles = self.controller.map_titles_from_model(tab_model)
        maps = self.controller.maps_from_model(tab_model)
        self._map_title_top.children = titles[0]
        self._map_title_bottom.children = titles[1]
        self._map_wrapper_top.children = [self._map_title_top, maps[0]]
        self._map_wrapper_bottom.children = [self._map_title_bottom, maps[1]]
        self._maps_area.children = [self._map_wrapper_top, self._map_wrapper_bottom]

    def close_tab(self, tab_model):
        for tab in self._tab_bar.children:
            if isinstance(tab, TabWithModel) and (tab.tab_model == tab_model):
                children = copy(self._tab_bar.children)
                children.remove(tab)
                self._tab_bar.children = children

    def maps(self) -> Optional[List[Map]]:
        if self._view_widgets_wrapper.children[0] == self._empty_text:
            return None

        map_wrapper_1 = self._maps_area.children[0]
        maps = [map_wrapper_1.children[1]]
        if len(self._maps_area.children) == 2:
            map_wrapper_2 = self._maps_area.children[1]
            maps.append(map_wrapper_2)

        return maps
