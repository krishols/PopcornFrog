import arcade
import arcade
from CONSTANTS import *
from Frog import FrogBody
from Popcorn import Popcorn
from random import randint
import arcade.key


class MovieTheaterFrog(arcade.Window, FrogBody):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None
        self.popsprite_list = None
        self.body = None
        self.timer = 1
        self.popcorn_counter = 0

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.popsprite_list = arcade.SpriteList()
        self.frogsprite_list.append(FrogBody())
        self.popsprite_list.append(Popcorn())
        self.body = self.frogsprite_list[0]

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.frogsprite_list.draw()
        arcade.draw_line(*self.body.tongue_args)
        self.popsprite_list.draw()

    def on_update(self, delta_time):
        self.frogsprite_list[0].update()
        self.popsprite_list.update()
        self.spawn_popcorn()
        self.update_timer()

    def spawn_popcorn(self):
        if self.timer % 100 == 0:
            self.popcorn_counter += 1
            self.popsprite_list.append(Popcorn())
            self.popsprite_list[self.popcorn_counter].center_x = randint(0,WINDOW_WIDTH)

    def update_timer(self):
        if self.timer < TIMER_MAX:
            self.timer += 1
        else:
            self.timer = 1



        """ Called every frame of the game (1/GAME_SPEED times per second)"""

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.frogsprite_list[0].change_x = MOVEMENT_SPEED
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.frogsprite_list[0].change_x = -MOVEMENT_SPEED

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.body.change_x = 0
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.body.change_x = 0

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.body.tongue_end_x = x
        self.body.tongue_end_y = y




def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()