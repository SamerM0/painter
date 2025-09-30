import cv2
import numpy as np
from drawing_modes import DrawingModes
import math
WINDOW_NAME = "Canvas"
ERASE_SIZE = 50
class Painter():
    def __init__(self,x,y,bgr_color,img_path = None):#initialize canvas
        self.current_mode = DrawingModes.NONE
        self.bgr_color = bgr_color
        if img_path is not None:
            self.__canvas = cv2.imread(img_path)
        else:
            self.__canvas = np.zeros((y, x, 3), dtype="uint8")
        self.__vertices = []
        self.is_drawing = False
        self.width = self.__canvas.shape[1]
        self.height = self.__canvas.shape[0]
        self.operations = [self.__canvas.copy()]
        self.undid_operations = []
        self.show_info()
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def set_mode(self, mode): #set drawing mode
        if self.is_drawing:
            return
        self.current_mode = mode
        self.show_info()

    def show_info(self):
        cv2.rectangle(self.__canvas,(0,0),(self.width,20),(255,255,255), -1)
        cv2.putText(self.__canvas, f"Mode: {self.current_mode.name} {str(' ' * 25)} Drawing : {self.is_drawing}", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1)
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def erase_info(self):#erase info box
        cv2.rectangle(self.__canvas,(0,0),(self.width,20),(0,0,0), -1)
        cv2.imshow(WINDOW_NAME, self.__canvas)

    def is_running(self):#check if window is open
        try:
            cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE)
            return True
        except cv2.error:
            return False

    def paint(self,verts,color = None,is_placeholder = False):#paint on canvas
        if color is None:
            color = self.bgr_color
        if self.current_mode == DrawingModes.CIRCLE:
            cv2.circle(self.__canvas, verts[0], math.ceil(math.dist(verts[0], verts[1])), color, -1)
        elif self.current_mode == DrawingModes.RECTANGLE:
            cv2.rectangle(self.__canvas, verts[0], verts[1], color, -1)
        elif self.current_mode == DrawingModes.POLYGON or self.current_mode == DrawingModes.CROP:
            points = np.array(verts)
            cv2.fillPoly(self.__canvas, [points], color)
        elif self.current_mode == DrawingModes.ERASE:
            x,y = verts[0]
            cv2.rectangle(self.__canvas, (x-ERASE_SIZE, y-ERASE_SIZE), (x+ERASE_SIZE, y+ERASE_SIZE), (0,0,0), -1)
        if is_placeholder:
            self.show_info()
            return
        self.add_operation() #add to stack
        #reset vertices and drawing state
        self.__vertices = []
        self.is_drawing = False
        self.show_info()
        
    def placeholder(self,x,y):#show placeholder while drawing
        if not self.is_drawing and self.current_mode != DrawingModes.CROP:
            return
        self.remove_placeholder()
        self.paint([*self.__vertices,[x,y]],color = (128,128,128),is_placeholder=True)
    def remove_placeholder(self):#remove placeholder 
        self.__canvas = self.operations[-1].copy()
        self.show_info()

    def add_point(self, x, y):#add point to vertices array
        if self.current_mode == DrawingModes.NONE:
            return
        self.start_drawing()
        self.__vertices.append([x, y])
        self.validate_paint()

    def validate_paint(self):#validate if enough points are added to paint
        if self.current_mode == DrawingModes.CIRCLE and len(self.__vertices) == 2:
            self.paint(self.__vertices)
        elif self.current_mode == DrawingModes.RECTANGLE and len(self.__vertices) == 2:
            self.paint(self.__vertices)
        elif self.current_mode == DrawingModes.POLYGON:
            return
        elif self.current_mode == DrawingModes.CROP and len(self.__vertices) == 4:
            self.crop()
        elif self.current_mode == DrawingModes.ERASE:
            self.paint(self.__vertices)

    def start_drawing(self):
        if self.is_drawing:
            return
        self.is_drawing = True
        self.show_info()

    def end_polygon(self):#end polygon drawing
        self.remove_placeholder()
        if self.current_mode != DrawingModes.POLYGON:
            return
        elif len(self.__vertices) > 2:
            self.paint(self.__vertices)
        
    def crop(self):#crop by creating a mask
        self.remove_placeholder()
        mask = np.zeros(self.__canvas.shape, dtype=np.uint8)
        points = np.array(self.__vertices)
        cv2.fillPoly(mask, [points], (255,255,255))
        cropped = cv2.bitwise_and(self.__canvas, mask)
        cv2.imshow("Cropped", cropped)
        self.__vertices = []
        self.is_drawing = False
        self.show_info()

    def rotate(self, angle):#rotate canvas using rotation matrix
        if self.is_drawing:
            return #cannot rotate while drawing
        self.erase_info()
        rotation_matrix = cv2.getRotationMatrix2D((self.width//2, (self.height-40)//2), angle, 1)
        self.__canvas = cv2.warpAffine(self.__canvas, rotation_matrix, (self.width, self.height-40))
        self.show_info()
        self.add_operation()

    def undo(self):
        if len(self.operations) < 2:
            print("No operation to undo")
            return
        self.undid_operations.append(self.operations.pop())
        self.__canvas = self.operations[-1].copy()
        self.show_info()

    def redo(self):
        if len(self.undid_operations) < 1:
            print("No operation to redo")
            return
        self.operations.append(self.undid_operations.pop())
        self.__canvas = self.operations[-1].copy()
        self.show_info()

    def add_operation(self):
        self.operations.append(self.__canvas.copy())
        self.undid_operations = []

    def free(self):
        cv2.destroyAllWindows()