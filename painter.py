import cv2
import numpy as np
from enum import Enum

WINDOW_NAME = "Canvas"
class Painter():
    def __init__(self,x,y,bgr_color):
        self.current_mode = DrawingModes.NONE
        self.bgr_color = bgr_color
        self.__canvas = np.zeros((x, y, 3), dtype="uint8")
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def set_mode(self, mode):
        self.current_mode = mode
        print("Changing mode to:", self.current_mode.name)

    def is_running(self):
        try:
            cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
            return True
        except cv2.error:
            return False

    def free(self):
        cv2.destroyAllWindows()

class DrawingModes(Enum):
    NONE = 0
    LINE = 1
    RECTANGLE = 2
    CIRCLE = 3
    POLYGON = 4
    ERASE = 5
    CROP = 6
    ROTATE = 7