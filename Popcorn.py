import arcade
from CONSTANTS import *
from random import randint

class Popcorn(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.center_y = WINDOW_HEIGHT
        self.center_x = WINDOW_WIDTH/2
        self.change_y = FALL_SPEED
        self.texture = POPCORN

    def update(self):
        self.center_y -= self.change_y







