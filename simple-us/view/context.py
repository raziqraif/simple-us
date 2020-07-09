from typing import List
from typing import Optional

from model import Experiment

DEFAULT_SELECTION = "Select"


class ViewContext:
    __id__ = 1

    def __init__(self, experiments: List[Experiment]):
        assert experiments is not None
        assert 1 <= len(experiments) <= 2
        if len(experiments) == 2:
            assert experiments[0].id_str != experiments[1].id_str
        self.experiments: List[Experiment] = experiments
        self.maps: any = []
        self.id = ViewContext.__id__
        ViewContext.__id__ += 1
        self._system_component: Optional[str] = None
        self._spatial_resolution: Optional[str] = None
        self._type_of_result: Optional[str] = None
        self._result_to_view: Optional[str] = None
        self._filter_lower_bound: Optional[str] = None
        self._filter_upper_bound: Optional[str] = None

    @property
    def is_comparison(self) -> bool:
        return len(self.experiments) == 2

    @property
    def is_display(self) -> bool:
        return len(self.experiments) == 1

    @property
    def title(self) -> str:
        if len(self.experiments) == 2:
            return "Compare - " + self.experiments[0].id_str + " & " + self.experiments[1].id_str
        return "Display - " + self.experiments[0].id_str

    @property
    def map_titles(self) -> List[str]:
        titles = ["Experiment: " + self.experiments[0].id_str + " - " + self.experiments[0].name]
        if len(self.experiments) == 2:
            title = ["Experiment: " + self.experiments[1].id_str + " - " + self.experiments[1].name]
            titles.append(title)
        return titles

    @property
    def system_component(self) -> str:
        return self._system_component if self._system_component is not None else DEFAULT_SELECTION

    @system_component.setter
    def system_component(self, value: str):
        self._system_component = value

    @property
    def spatial_resolution(self) -> str:
        return self._spatial_resolution if self._spatial_resolution is not None else DEFAULT_SELECTION

    @spatial_resolution.setter
    def spatial_resolution(self, value: str):
        self._spatial_resolution = value

    @property
    def type_of_result(self) -> str:
        return self._type_of_result if self._type_of_result is not None else DEFAULT_SELECTION

    @type_of_result.setter
    def type_of_result(self, value: str):
        self._spatial_resolution = value

    @property
    def result_to_view(self) -> str:
        return self._result_to_view if self._result_to_view is not None else DEFAULT_SELECTION

    @result_to_view.setter
    def result_to_view(self, value: str):
        self._result_to_view = value

    @property
    def filter_lower_bound(self) -> float:
        return self._filter_lower_bound if self._filter_lower_bound is not None else 0.0

    @filter_lower_bound.setter
    def filter_lower_bound(self, value: str):
        self._filter_lower_bound = value

    @property
    def filter_upper_bound(self) -> float:
        return self._filter_upper_bound if self._filter_upper_bound is not None else 100.0

    @filter_upper_bound.setter
    def filter_upper_bound(self, value: str):
        self._filter_upper_bound = value
