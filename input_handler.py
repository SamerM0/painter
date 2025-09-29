import cv2
from drawing_modes import DrawingModes
from painter import Painter
class InputHandler():
    def __init__(self, painter : Painter):
        self.painter = painter
        cv2.setMouseCallback("Canvas", self.mouse_listener)
    def start(self):
        while self.painter.is_running():
            key = cv2.waitKey(0)
            if key & 0xFF == 27:  # ESC key
                self.painter.free()
                break
            elif key & 0xFF == ord("c"):
                self.painter.set_mode(DrawingModes.CIRCLE)
            elif key & 0xFF == ord("r"):
                self.painter.set_mode(DrawingModes.RECTANGLE)
            elif key & 0xFF == ord("p"):
                self.painter.set_mode(DrawingModes.POLYGON)
            elif key & 0xFF == ord("s"):
                self.painter.end_polygon()
            elif key & 0xFF == ord("e"):
                self.painter.set_mode(DrawingModes.ERASE)
            elif key & 0xFF == ord("x"):
                self.painter.set_mode(DrawingModes.CROP)
            elif key & 0xFF == ord("a"):
                self.painter.rotate(90)
            elif key & 0xFF == ord("d"):
                self.painter.rotate(-90)
            elif key & 0xFF == ord("u"):
                self.painter.undo()
            elif key & 0xFF == ord("i"):
                self.painter.redo()
    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.painter.add_point(x,y)
        #if event == cv2.EVENT_MOUSEMOVE:
        #    self.painter.placeholder(x,y)