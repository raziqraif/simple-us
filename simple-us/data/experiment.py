from __future__ import annotations
from typing import Optional


class Experiment:
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


if __name__ == "__main__":
    Experiment()
