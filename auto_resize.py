from win32api import GetSystemMetrics


class auto_resize():
    def __init__(self):
        self.screen = (GetSystemMetrics(0),GetSystemMetrics(1))
        self.scale_x = ()