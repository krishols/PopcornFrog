import arcade
from CONSTANTS import *


class FrogBody(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y= 100
        self.texture = FROG



