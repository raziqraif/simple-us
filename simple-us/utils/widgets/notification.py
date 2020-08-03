from typing import Optional

from ipymaterialui import Snackbar, IconButton, Icon, Container
from ipymaterialui import SnackbarContent


# https://material-ui.com/customization/palette/
ERROR_COLOR = "#f44336"
INFO_COLOR = "#2196f3"
SUCCESS_COLOR = "#4caf50"
WARNING_COLOR = "#ff9800"

# Only two instances of this class will be maintained and they will spawn alternatingly, because:
# - instantiating it is slow
# - consecutive notification (Snackbar widget) needs to have a distinct key to ensure smooth transition.


class Notification(Snackbar):
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    ERROR = "error"
    MODES = [SUCCESS, WARNING, INFO, ERROR]

    MANAGE_PAGE = "manage_page"
    CREATE_PAGE = "create_page"
    VIEW_PAGE = "view_page"
    ABOUT_PAGE = "about_page"
    PAGES = [MANAGE_PAGE, CREATE_PAGE, VIEW_PAGE, ABOUT_PAGE]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._content: Optional[SnackbarContent] = None

        self._text = "Initial notification"
        self._mode = self.INFO
        self._page = self.CREATE_PAGE

        self.open_ = False
        self.key = id(self)
        self.auto_hide_duration = 2000
        self.anchor_origin = {"horizontal": "center", "vertical": "top"}
        self.style_ = self._get_root_style()
        self.transition_duration = 100

        self.on_event("onClose", self._on_close)
        self._build_content()

        self.action = self._create_close_button()
        self.children = self._content

    def _get_root_style(self) -> dict:
        style_ = {
            "display": "flex",
            "flex-direction": "row",
            "justify-contents": "center",
            "align-items": "center",
            "padding": "0px 0px 0px 0px",
            "height": "50px",
            # "background": "{}".format(self._get_background_color()),
            "margin": "{}".format(self._get_margin()),
            "border-radius": "5px",
        }
        return style_

    def _get_content_style(self) -> dict:
        style_ = {
            "display": "flex",
            "flex-direction": "row",
            "justify-contents": "center",
            "align-items": "center",
            "height": "50px",
            "background": "{}".format(self._get_background_color()),
        }
        return style_

    def _get_margin(self):
        # TODO: Change this depending on the page
        if self._page == Notification.MANAGE_PAGE:
            return "140px 0px 0px 0px"
        elif self._page == Notification.CREATE_PAGE:
            return "160px 0px 0px 0px"

        else:
            return "140px 0px 0px 0px"

    def _build_content(self):
        text_wrapper = self._create_text_wrapper()
        self._content = SnackbarContent(message=text_wrapper,
                                        action=self._create_close_button(),
                                        style_=self._get_content_style())

    def _create_text_wrapper(self):
        from .. import CustomText
        text_html = CustomText(self._text, style_={"color": "white", "padding":"0px 0px 0px 8px"})
        icon = Icon(children=self._get_icon_name())
        text_wrapper = Container(children=[icon, text_html],
                                 style_={
                                     "display": "flex",
                                     "flex-direction": "row",
                                     "flex-grow": "1",
                                     "justify-contents": "flex-start",
                                     "align-items": "center",
                                     "padding": "0px 0px 0px 0px",
                                 })
        return text_wrapper

    def _create_close_button(self) -> IconButton:
        icon = Icon(children="close", style_={"color": "white", "font-size": "18px"})
        button = IconButton(children=icon)
        button.on_event("onClick", self._on_close)
        return button

    def _get_icon_name(self):
        if self._mode == self.ERROR:
            return "error_outlined"
        elif self._mode == self.INFO:
            return "info_outlined"
        elif self._mode == self.SUCCESS:
            return "done_all"
        elif self._mode == self.WARNING:
            return "warning_outlined"
        else:
            raise Exception("Invalid notfication mode")

    def _get_background_color(self) -> str:
        if self._mode == self.ERROR:
            return ERROR_COLOR
        elif self._mode == self.INFO:
            return INFO_COLOR
        elif self._mode == self.SUCCESS:
            return SUCCESS_COLOR
        elif self._mode == self.WARNING:
            return WARNING_COLOR
        else:
            raise Exception("Invalid notfication mode")

    def _on_close(self, widget, event, data):
        self.open_ = False

    def show(self, text: str, mode: str, page: str):
        assert mode in self.MODES
        assert page in self.PAGES

        self._text = text
        self._mode = mode
        self._page = page
        self.style_ = self._get_root_style()
        self._content.message = self._create_text_wrapper()
        self._content.style_ = self._get_content_style()
        self.open_ = True
