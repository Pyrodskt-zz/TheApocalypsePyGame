from win32api import GetSystemMetrics
import math

class Size:
    def __init__(self, height, width):
        self.screen = (height, width)
        self.scale_x = (float(self.screen[0]) / 1080.0)
        self.scale_y = (float(self.screen[1]) / 720.0)

    def calc_x(self, size):
        return math.ceil(size * self.scale_x)

    def calc_y(self, size):
        return math.ceil(size * self.scale_y)