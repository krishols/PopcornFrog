from CONSTANTS import *
class Table(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y= 50
        self.texture = TABLE