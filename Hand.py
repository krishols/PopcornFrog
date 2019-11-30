from CONSTANTS import *
import arcade

class HandBoss(arcade.Sprite):
    """Creates hand bosses"""

    def __init__(self):
        super().__init__()
        self.center_y = WINDOW_HEIGHT
        self.center_x = WINDOW_WIDTH/2
        self.texture = HAND
        self.change_x = MOVEMENT_SPEED
        self.change_y = 1
        self.scale = 2.25

    def move_right(self):
        self.center_x += self.change_x

    def move_left(self):
        self.center_x -= self.change_x

    def update(self):
        self.center_y -= self.change_y




