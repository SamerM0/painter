import cv2
from painter import Painter, DrawingModes
class InputHandler():
    def __init__(self, painter : Painter):
        self.painter = painter
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
