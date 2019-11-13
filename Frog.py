import arcade
from CONSTANTS import *


class FrogBody(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y= 100
        self.texture = FROG
        self.change_x = 0

    def update(self):
        self.center_x += self.change_x
        if self.center_x <= 0 or self.center_x >= WINDOW_WIDTH:
            self.change_x = 0










