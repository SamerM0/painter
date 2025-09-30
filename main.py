from painter import Painter
from input_handler import InputHandler
from tkinter import filedialog
def main():
    #x,y = 700,900
    #bgr_color = (255,0,0)
    img_to_edit = None
    if input("Edit an image? (y/n): ").lower() == 'y':
        img_to_edit = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico"), ("All files", "*.*")])
    else:
        x,y = get_resolution()
    bgr_color = get_color()

    if img_to_edit: # check if path is correct
        painter = Painter(0, 0, bgr_color, img_path=img_to_edit)
    else:
        painter = Painter(x,y,bgr_color)

    input_handler = InputHandler(painter)
    input_handler.start()
    painter.free()
    
def get_resolution():
    res = input("Enter resolution (x y): ")
    width, height = map(int, res.split())
    return (width, height)

def get_color():
    color = input("Enter a color (b g r): ")
    b,g,r = map(int, color.split())
    return (b, g, r)

if __name__ == "__main__":
    main()