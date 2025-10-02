import cv2
from drawing_modes import DrawingModes
from painter import Painter
from tkinter import filedialog

class InputHandler():
    def setup(self, painter : Painter):
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
                self.painter.rotate(False)
            elif key & 0xFF == ord("d"):
                self.painter.rotate(True)
                
            elif key & 0xFF == ord("u"):
                self.painter.undo()
            elif key & 0xFF == ord("i"):
                self.painter.redo()

    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.painter.add_point(x,y)
        elif event == cv2.EVENT_MOUSEMOVE:
            self.painter.placeholder(x,y)

    def get_resolution(self):
        res = input("Enter resolution (x y): ")
        width, height = map(int, res.split())
        return (width, height)

    def get_color(self):
        color = input("Enter a color (b g r): ")
        b,g,r = map(int, color.split())
        return (b, g, r)

    def get_image_path(self):
        path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico"), ("All files", "*.*")])
        return path
    
    def check_for_dedicated_info_window(self):
        use_info_window = input("Use dedicated info window? (y/n): ").lower() == 'y'
        return use_info_window