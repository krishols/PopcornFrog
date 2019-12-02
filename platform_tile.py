from CONSTANTS import *


class platform_tile(arcade.Sprite):
    """Creates platforms for frog to jump on"""
    def __init__(self):
        super().__init__()
        self.center_x = WINDOW_WIDTH/2
        self.texture = PLATFORM_TILE