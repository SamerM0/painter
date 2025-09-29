import cv2
from painter import Painter, DrawingModes
class InputHandler():
    def __init__(self, painter : Painter):
        self.painter = painter
        cv2.setMouseCallback("Canvas", self.mouse_listener)
    def start(self):
        while self.painter.is_running():
            key = cv2.waitKey(0)
            print(f"key pressed: {key}")
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
    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.painter.add_point(x,y)
        #if event == cv2.EVENT_MOUSEMOVE:
        #    self.painter.placeholder(x,y)