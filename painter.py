import cv2
import numpy as np
from enum import Enum
import math
WINDOW_NAME = "Canvas"
SIZE_CONSTANT = 20
class Painter():
    def __init__(self,x,y,bgr_color):
        self.current_mode = DrawingModes.NONE
        self.bgr_color = bgr_color
        self.__canvas = np.zeros((x, y, 3), dtype="uint8")
        self.__scale = 1.0
        cv2.rectangle(self.__canvas,(0,0),(self.__canvas.shape[0],40),(255,255,255), -1)
        cv2.putText(self.__canvas, f"Mode: {self.current_mode.name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1)
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def set_mode(self, mode):
        self.current_mode = mode
        cv2.rectangle(self.__canvas,(0,0),(self.__canvas.shape[0],40),(255,255,255), -1)
        cv2.putText(self.__canvas, f"Mode: {self.current_mode.name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1)
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def is_running(self):
        try:
            cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
            return True
        except cv2.error:
            return False

    def paint(self, x, y):
        if self.current_mode == DrawingModes.CIRCLE:
            cv2.circle(self.__canvas, (x, y), math.ceil(self.__scale * SIZE_CONSTANT), self.bgr_color, -1)
        elif self.current_mode == DrawingModes.RECTANGLE:
            cv2.rectangle(self.__canvas,(math.ceil(x-self.__scale * SIZE_CONSTANT),math.ceil(y-self.__scale * SIZE_CONSTANT)),(math.ceil(x+self.__scale * SIZE_CONSTANT),math.ceil(y+self.__scale * SIZE_CONSTANT)), self.bgr_color, -1)
        cv2.imshow(WINDOW_NAME, self.__canvas)
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