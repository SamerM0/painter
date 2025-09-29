import cv2
import numpy as np
from enum import Enum
import math
WINDOW_NAME = "Canvas"
ERASE_SIZE = 50
class Painter():
    def __init__(self,x,y,bgr_color):#initialize canvas
        self.current_mode = DrawingModes.NONE
        self.bgr_color = bgr_color
        self.__canvas = np.zeros((x, y, 3), dtype="uint8")
        self.__vertices = []
        self.is_drawing = False
        self.show_info()
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def set_mode(self, mode): #set drawing mode
        if self.is_drawing:
            return
        self.current_mode = mode
        self.show_info()

    def show_info(self):
        cv2.rectangle(self.__canvas,(0,0),(self.__canvas.shape[0],40),(255,255,255), -1)
        cv2.putText(self.__canvas, f"Mode: {self.current_mode.name} {str(' ' * 25)} Drawing : {self.is_drawing}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1)
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def is_running(self):
        try:
            cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
            return True
        except cv2.error:
            return False

    def paint(self):#paint on canvas
        if self.current_mode == DrawingModes.CIRCLE:
            cv2.circle(self.__canvas, self.__vertices[0], math.ceil(math.dist(self.__vertices[0], self.__vertices[1])), self.bgr_color, -1)
        elif self.current_mode == DrawingModes.RECTANGLE:
            cv2.rectangle(self.__canvas, self.__vertices[0], self.__vertices[1], self.bgr_color, -1)
        elif self.current_mode == DrawingModes.POLYGON:
            points = np.array(self.__vertices)
            cv2.fillPoly(self.__canvas, [points], self.bgr_color)
        elif self.current_mode == DrawingModes.ERASE:
            x,y = self.__vertices[0]
            cv2.rectangle(self.__canvas, (x-ERASE_SIZE, y-ERASE_SIZE), (x+ERASE_SIZE, y+ERASE_SIZE), (0,0,0), -1)

        #reset vertices and drawing state
        self.__vertices = []
        self.is_drawing = False
        self.show_info()
        

    def add_point(self, x, y):#add point to vertices array
        if self.current_mode == DrawingModes.NONE:
            return
        self.start_drawing()
        self.__vertices.append([x, y])
        self.validate_paint()

    def validate_paint(self):#validate if enough points are added to paint
        if self.current_mode == DrawingModes.CIRCLE and len(self.__vertices) == 2:
            self.paint()
        elif self.current_mode == DrawingModes.RECTANGLE and len(self.__vertices) == 2:
            self.paint()
        elif self.current_mode == DrawingModes.POLYGON:
            return
        elif self.current_mode == DrawingModes.ERASE:
            self.paint()
        
    def start_drawing(self):
        if self.is_drawing:
            return
        self.is_drawing = True
        self.show_info()

    def end_polygon(self):#end polygon drawing
        if self.current_mode != DrawingModes.POLYGON:
            return
        elif len(self.__vertices) > 2:
            self.paint()
    
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