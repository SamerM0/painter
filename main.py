from painter import Painter
from input_handler import InputHandler
import time
def main():
    painter = Painter(700,700)
    input_handler = InputHandler(painter)
    input_handler.start()
    painter.free()
    

if __name__ == "__main__":
    main()