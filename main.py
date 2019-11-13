import arcade
import arcade
from CONSTANTS import *
from Frog import FrogBody
import arcade.key


class MovieTheaterFrog(arcade.Window, FrogBody):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None
        self.body = None

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.frogsprite_list.append(FrogBody())
        self.body = self.frogsprite_list[0]

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.frogsprite_list.draw()

    def on_update(self, delta_time):
        self.frogsprite_list[0].update()

        """ Called every frame of the game (1/GAME_SPEED times per second)"""

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.frogsprite_list[0].change_x = MOVEMENT_SPEED
        elif symbol == arcade.key.A:
            self.frogsprite_list[0].change_x = -MOVEMENT_SPEED

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.body.change_x = 0
        elif symbol == arcade.key.A:
            self.body.change_x = 0




def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()