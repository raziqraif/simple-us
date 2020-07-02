from typing import Optional

import model as model_pkg
from database import DBManager


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

    """ Some html components expect a string value. So, the following are helper methods for that """

    @property
    def id_str(self) -> str:
        return Experiment.to_id_str(self.id)

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
        # TODO: Needs to return "SHARED" or "PUBLIC"
        return str(self.submission_time) if self.submission_time is not None else ""

    @staticmethod
    def to_id(id_str: str) -> int:
        # TODO: Update this
        return int(id_str)

    @staticmethod
    def to_id_str(id_: int, is_private=True) -> str:
        # TODO: Update this
        return str(id_)

    @staticmethod
    def is_private_id_str(id_str) -> bool:
        return True  # TODO: Update this

    @staticmethod
    def is_shared_id_str(id_str) -> bool:
        return False  # TODO: Update this

    @staticmethod
    def from_id_str(id_str: str) -> Optional[model_pkg.Experiment]:
        id_ = Experiment.to_id(id_str)
        is_private = Experiment.is_private_id_str(id_str)
        exp = Experiment.from_id(id_, is_private)
        return exp

    @staticmethod
    def from_id(id_: int, is_private: bool) -> Optional[model_pkg.Experiment]:
        db = DBManager(private_experiments=is_private)
        exp = db.get_experiment(id_)
        return exp


if __name__ == "__main__":
    Experiment()
