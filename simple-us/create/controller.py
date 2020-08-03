from pathlib import Path

from utils.experimentutil import ExperimentManager
from utils.pubsubmessage import sendMessage, NOTIFICATION_CREATED, DATABASE_MODIFIED
from utils.widgets.notification import Notification


class CreateTab:
    def __init__(self):
        from .view import CreateTabView
        self.view = CreateTabView(self)
        self._uploaded_file_path = Path("test")  # TODO: Update this

    def onclick_upload(self):
        pass

    def onclick_submit(self, widget, event, data):
        if not self._validate_form():
            return
        model = self.view.model
        name = self.view.name
        description = self.view.description
        success, experiment = ExperimentManager.submit_experiment(model=model, name=name, description=description)
        if success:
            sendMessage(DATABASE_MODIFIED)
            self.view.clear_form()
            self._uploaded_file_path = None
            text = "Experiment has been submitted"
            sendMessage(NOTIFICATION_CREATED, text=text, mode=Notification.SUCCESS, page=Notification.CREATE_PAGE)
        else:
            text = "Experiment failed to be submitted"
            sendMessage(NOTIFICATION_CREATED, text=text, mode=Notification.ERROR, page=Notification.CREATE_PAGE)

    def _validate_form(self):
        # TODO: Validate config file
        model = self.view.model
        name = self.view.name
        description = self.view.description
        text = None
        if model == "":
            text = "Model cannot be empty"
        elif name == "":
            text = "Name cannot be empty"
        elif len(name) > 35:
            text = "Name cannot have more than 35 characters"
        elif description == "":
            text = "Description cannot be empty"
        elif len(description) > 300:
            text = "Description cannot have more than 300 characters"
        elif self._uploaded_file_path is None:
            text = "Please upload a configuration file"
        if text is not None:
            sendMessage(NOTIFICATION_CREATED, text=text, mode=Notification.WARNING,
                        page=Notification.CREATE_PAGE)
            return False
        return True
