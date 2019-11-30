import arcade
from CONSTANTS import *

class RisingPopcorn(arcade.Sprite):
    """Creates the rising popcorn sprite"""
    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y = -300
        self.change_y = RISE_SPEED
        self.texture = RISING_POPCORN

    def update(self):
        self.center_y += self.change_y


