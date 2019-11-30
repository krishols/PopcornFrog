import arcade
from CONSTANTS import *

class CandyFall(arcade.Sprite):
    """Creates candy sprites"""
    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT
        self.change_y = FALL_SPEED
        self.texture = CANDY

    def update(self):
        self.center_y -= self.change_y