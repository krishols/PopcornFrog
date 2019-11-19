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
        self.off_screen = False

    def update(self):
        self.center_y -= self.change_y
        self.off_screen_test()

    def off_screen_test(self):
        if self.center_y < 0:
            self.off_screen = True
        else:
            self.off_screen = False
        return self.off_screen







