import re
import os
from pathlib import Path
from typing import Optional, List

from utils import SIMPLEUtil


class Experiment:
    """ Class to represent the SIMPLEJobs db table

    Values are stored as they are read from the the db. Helper functions are used if the values
    need to be transformed.
    """

    def __init__(self,
                 id: int = -1,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 description: Optional[str] = None,
                 model: Optional[str] = None,
                 submission_id: Optional[str] = None,
                 submission_time: Optional[str] = None,
                 published: Optional[int] = None,
                 author: Optional[str] = None,
                 ):
        self.id = id
        self.name = name
        self.status = status
        self.model = model
        self.description = description
        self.author = author
        self.submission_id = submission_id
        self.submission_time = submission_time
        self.published = published
        self._is_private = self.published != 1

    """ General property methods """

    @property
    def id_str(self) -> str:
        return Experiment.to_id_str(self.id, self._is_private)

    @property
    def name_str(self) -> str:
        return self.name if self.name is not None else ""

    @property
    def status_str(self) -> str:
        return self.status if self.status is not None else ""

    @property
    def model_str(self) -> str:
        return self.model if self.model is not None else ""

    @property
    def description_str(self) -> str:
        return self.description if self.description is not None else ""

    @property
    def author_str(self) -> str:
        return self.author if self.author is not None else ""

    @property
    def submission_id_str(self) -> str:
        return self.submission_id if self.submission_id is not None else ""

    @property
    def submission_time_str(self) -> str:
        return self.submission_time if self.submission_time is not None else ""

    @property
    def published_str(self) -> str:
        return "No" if self.is_private else "Yes"

    @property
    def is_private(self):
        return Experiment.is_private_id_str(self.id_str)

    @property
    def is_completed(self):
        return self.status_str.lower() == "completed"

    @staticmethod
    def to_id(id_str: str) -> int:
        id_ = int(id_str[1:])
        return id_

    @staticmethod
    def to_id_str(id_: int, is_private: bool) -> str:
        return "P" + str(id_) if is_private else "S" + str(id_)

    @staticmethod
    def is_private_id_str(id_str: str) -> bool:
        return id_str[0] == "P"

    @staticmethod
    def is_shared_id_str(id_str: str) -> bool:
        return id_str[0] == "S"

    @staticmethod
    def from_id_str(id_str: str):  # Python 3.7 doesn't support future annotation. So, cannot annotate return type
        exp = Experiment.from_id(id_str)
        return exp

    @staticmethod
    def from_id(id_: int, is_private: bool):
        from database import DBManager
        id_str = Experiment.to_id_str(id_, is_private)
        db = DBManager()
        exp = db.get_experiment(id_str)
        return exp


if __name__ == "__main__":
    e1 = Experiment(1)
    e2 = Experiment(2)
