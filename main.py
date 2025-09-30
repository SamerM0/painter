from painter import Painter
from input_handler import InputHandler
def main():
    #x,y = 700,900
    #bgr_color = (255,0,0)
    input_handler = InputHandler()
    img_to_edit = None
    if input("Edit an image? (y/n): ").lower() == 'y':
        img_to_edit = input_handler.get_image_path()
    else:
        x,y = input_handler.get_resolution()

    bgr_color = input_handler.get_color()

    if img_to_edit: # check if path is correct
        painter = Painter(0, 0, bgr_color, img_path=img_to_edit)
    else:
        painter = Painter(x,y,bgr_color)

    input_handler.setup(painter)
    input_handler.start()
    painter.free()

if __name__ == "__main__":
    main()