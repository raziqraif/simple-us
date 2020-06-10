from datetime import datetime


class Experiment:
    def __init__(self,
                 id: int = 0,
                 name: str = "Untitled",
                 status: str = "Unknown status",
                 description: str = "-",
                 model: str = "Unknown model",
                 submission_id: int = 0,
                 submission_time: datetime = datetime.now()):

        self.id = id
        self.name = name
        self.status = status
        self.description = description
        self.model = model
        self.submission_id = submission_id
        self.submission_time = submission_time
