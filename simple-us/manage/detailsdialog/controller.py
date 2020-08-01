from IPython.display import display
from ipymaterialui import Paper


class Details:
    def __init__(self):
        from .view import DetailsView  # Avoid circular dependency
        self.view = DetailsView(self)
        self._backdrop_was_clicked = True
        # display(self.view)

    def onclose(self, widget, event, data):
        self.view.close()

    def onclick_backdrop(self, widget, event, data):
        # The following conditions are needed because clicking on the dialog's "body" would call this method twice.
        # The first call has a "Paper" object as the widget arg and the second call has a "DetailsView" object as the
        # widget arg.
        # Clicking on the backdrop will only fire call this method once, with a "DetailsView" object as the widget arg.
        if isinstance(widget, Paper):
            self._backdrop_was_clicked = False
            return

        from .view import DetailsView
        if isinstance(widget, DetailsView):
            if not self._backdrop_was_clicked:
                self._backdrop_was_clicked = True
                return

            self.view.close()
