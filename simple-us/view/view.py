from copy import copy, deepcopy
from typing import List
from typing import Optional

from ipyleaflet import Map, Path, TileLayer
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
from ipywidgets import Layout, jslink

from .viewcontext import ViewContext
from .controller import ViewTab
from .sidebar import SidebarView
from map import CustomMap
from utils import CustomText
from utils import INNER_BACKGROUND_COLOR
from utils import PRIMARY_COLOR_LIGHT
from utils import PRIMARY_COLOR


class TabWithContext(Tab):
    def __init__(self, context: ViewContext = None, **kwargs):
        super().__init__(**kwargs)
        self.context: ViewContext = context


class ViewTabUI(Container):

    def __init__(self, controller: ViewTab, sidebar: SidebarView, **kwargs):
        super().__init__(**kwargs)

        self.controller: ViewTab = controller

        self._tab_bar: Optional[Container] = None
        self._body: Optional[Container] = None  # contains view widgets wrapper
        self._view_widgets_wrapper: Optional[Container] = None  # contains sidebar and maps area / "no experiment" label
        self._sidebar: SidebarView = sidebar
        self._maps_area: Optional[Container] = None  # contains maps and titles

        self._map_title_full: Optional[CustomText]
        self._map_title_top: Optional[CustomText] = None
        self._map_title_bottom: Optional[CustomText] = None
        self._map_wrapper_full: Optional[Container] = None
        self._map_wrapper_top: Optional[Container] = None
        self._map_wrapper_bottom: Optional[Container] = None

        self._default_tab: Optional[TabWithContext] = None
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
            "width": "1090px",
            "border": "1px solid " + PRIMARY_COLOR,
            "height": "750px",
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
        self._body = Container(children=[self._empty_text],
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
        self.children = [self._tab_bar, self._body]

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
            centered=False, tab_model=0,
        )
        self._tab_bar.observe(self.controller.onchange_tab, 'value')

    def _build_maps_area(self):
        self._map_title_full = CustomText("", style_={"font-weight": "bold",
                                                      "font-size": "14px",
                                                      "padding": "0px 0px 0px 0px",
                                                      "margin": "0px 0px 0px 0px",
                                                      "align-self": "flex-start",
                                                      "width": "100%",
                                                      })
        self._map_title_top = CustomText("", style_={"font-weight": "bold",
                                                     "font-size": "14px",
                                                     "padding": "0px 0px 0px 0px",
                                                     "margin": "0px 0px 0px 0px",
                                                     "align-self": "flex-start",
                                                     "width": "100%",
                                                     })
        self._map_title_bottom = CustomText("", style_={"font-weight": "bold",
                                                        "font-size": "14px",
                                                        "padding": "0px 0px 0px 0px",
                                                        "margin": "8px 0px 0px 0px",
                                                        "align-self": "flex-start",
                                                        "width": "100%",
                                                        })
        self._map_wrapper_full = self._create_map_wrapper(self._map_title_full)
        self._map_wrapper_top = self._create_map_wrapper(self._map_title_top, False)
        self._map_wrapper_bottom = self._create_map_wrapper(self._map_title_bottom, False)
        initial_maps_area = Container(children=[""],
                                      style_={
                                          "display": "flex",
                                          "flex-direction": "column",
                                          "justify-content": "flex-start",
                                          "align-items": "center",
                                          "align-self": "center",
                                          "padding": "0px 0px 0px 0px",
                                          "margin": "0px 0px 0px 16px",
                                          "width": "720px",
                                          "height": "640px",
                                          # "width": "100%",
                                          # "height": "480px",
                                      })
        self._maps_area = initial_maps_area

    def _create_map_wrapper(self, title, full_height=True) -> Container:
        height = "640px" if full_height else "316px"
        wrapper = Container(children=[title],
                            style_={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "flex-start",
                                "align-items": "center",
                                "width": "100%",
                                "height": height,
                                "padding": "0px 0px 0px 0px",
                                "margin": "0px 0px 0px 0px",
                            })
        return wrapper

    def _create_empty_map(self, full_height=True):
        height = "614px" if full_height else "290px"
        # layout = Layout(width="600px", height=height)
        return CustomMap("720px", height)
        # return Map(layout=layout, center=(39.5, -98.35), zoom=4)  # TODO: Update this

    def new_tab(self, tab_name: str, tab_model: any, comparison: bool = False):
        children = self._tab_bar.children
        children = copy(children) if children[0] != self._default_tab else []  # copy() is needed.
        # It seems like if the memory address of children is the same, the DOM will not get updated.

        tab = TabWithContext(label=CustomText(tab_name,
                                              style_={
                                                "color": "#ffffff",
                                                "padding": "0px 0px 0px 0px",
                                            }), context=tab_model, selected=True)
        children.append(tab)
        self._tab_bar.children = children
        if comparison:
            maps = [self._create_empty_map(full_height=False) for count in range(2)]
        else:
            maps = [self._create_empty_map()]
        self.controller.cache_maps(maps, tab_model)
        self._tab_bar.value = len(children) - 1  # onchange_tab will trigger after this line

    def show_maps(self, context: ViewContext):
        assert isinstance(context, ViewContext)
        maps = context.maps
        assert 1 <= len(maps) <= 2
        assert isinstance(maps[0], Map)

        if len(maps) == 1:
            self._show_full_map(context)
        elif len(maps) == 2:
            self._show_comparison_maps(context)

    def _show_full_map(self, context: ViewContext):
        assert isinstance(context, ViewContext)

        if self._body.children[0] == self._empty_text:
            self._body.children = [self._view_widgets_wrapper]
        title = context.map_titles[0]
        map_: CustomMap = context.maps[0]
        self._map_title_full.children = title
        self._map_wrapper_full.children = [self._map_title_full, map_]
        self._maps_area.children = [self._map_wrapper_full]

    def _show_comparison_maps(self, context: ViewContext):
        if self._body.children[0] == self._empty_text:
            self._body.children = [self._view_widgets_wrapper]
        titles = context.map_titles
        maps = context.maps
        self._map_title_top.children = titles[0]
        self._map_title_bottom.children = titles[1]
        self._map_wrapper_top.children = [self._map_title_top, maps[0]]
        self._map_wrapper_bottom.children = [self._map_title_bottom, maps[1]]
        self._maps_area.children = [self._map_wrapper_top, self._map_wrapper_bottom]
        maps[0].link(maps[1])
        maps[1].link(maps[0])

    def _show_empty_text(self):
        self._body.children = [self._empty_text]

    def close_tab(self, tab_model):
        for tab in self._tab_bar.children:
            if isinstance(tab, TabWithContext) and (tab.context == tab_model):
                children = copy(self._tab_bar.children)
                children.remove(tab)
                self._tab_bar.children = children

        self._show_empty_text()

    def maps(self) -> Optional[List[CustomMap]]:
        if self._body.children[0] == self._empty_text:
            return None

        if len(self._maps_area.children) == 1:
            maps = [self._map_wrapper_full.children[1]]
        else:
            maps = [
                self._map_wrapper_top.children[1],
                self._map_wrapper_bottom.children[1]
            ]
        return maps

    def context(self, tab_index: int) -> ViewContext:
        assert 0 <= tab_index <= len(self._tab_bar.children) - 1
        tab: TabWithContext = self._tab_bar.children[tab_index]
        assert isinstance(tab, TabWithContext)
        return tab.context
