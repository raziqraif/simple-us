from __future__ import annotations
from typing import Optional


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
        return str(self.id)

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


if __name__ == "__main__":
    Experiment()
