import arcade
from CONSTANTS import *


class FrogBody(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.center_y= 100
        self.texture = FROG
        self.change_x = 0
        self.tongue_end_x = self.center_x + 100
        self.tongue_end_y = self.center_y + 100
        self.tongue_args =  [
            self.center_x,
            self.center_y,
            self.tongue_end_x,
            self.tongue_end_y,
            [255, 192, 203],
            5
        ]


    def update(self):
        self.center_x += self.change_x
        if self.center_x <= 0 or self.center_x >= WINDOW_WIDTH:
            self.change_x = 0
        self.tongue()

    def tongue(self):
        self.tongue_args = [
            self.center_x,
            self.center_y,
            self.tongue_end_x,
            self.tongue_end_y,
            [255, 192, 203],
            5

        ]













