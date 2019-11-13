import arcade
import arcade
from CONSTANTS import *
from Frog import FrogBody


class MovieTheaterFrog(arcade.Window, FrogBody):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.frogsprite_list.append(FrogBody())

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.frogsprite_list.draw()

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""


def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()