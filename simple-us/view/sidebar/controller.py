

class Sidebar:
    def __init__(self):
        from .view import SidebarView
        self.view = SidebarView(self)

    def system_components(self):
        return ["", "test", "test", "test"]

    def spatial_resolution(self):
        return ["", "test", "test", "test"]

    def type_of_results(self):
        return ["", "test", "test", "test"]

    def result_to_view(self):
        return ["", "test", "test", "test"]
