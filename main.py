from painter import Painter
from input_handler import InputHandler
import time
def main():
    #x,y = get_resolution()
    #bgr_color = get_color()
    x,y = 500,500
    bgr_color = (255,0,0)
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