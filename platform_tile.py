from CONSTANTS import *


class PlatformTile(arcade.Sprite):
    """Creates platforms for frog to jump on"""
    def __init__(self):
        super().__init__()
        self.texture = PLATFORM_TILE