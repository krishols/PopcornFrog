from CONSTANTS import *


class platform_tile(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y= 200
        self.texture = PLATFORM_TILE