import arcade
from CONSTANTS import *
from Frog import FrogBody
from Popcorn import Popcorn
from random import randint
from Candy import CandyFall
import arcade.key



class MovieTheaterFrog(arcade.Window, FrogBody):
    def __init__(self, x=0, y=0):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None
        self.popsprite_list = None
        self.body = None
        self.timer = 1
        self.popcorn_counter = 0
        self.score = 0
        self.popcorn = []
        self.tongue_end_x = x
        self.tongue_end_y = y
        self.score = 0
        self.candysprite_list = None
        self.candy_counter = 0

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.popsprite_list = arcade.SpriteList()
        self.candysprite_list = arcade.SpriteList()
        self.candysprite_list.append(CandyFall())
        self.frogsprite_list.append(FrogBody())
        self.popsprite_list.append(Popcorn())
        self.body = self.frogsprite_list[0]




    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.frogsprite_list.draw()
        arcade.draw_line(*self.body.tongue_args)
        self.popsprite_list.draw()
        self.candysprite_list.draw()
        arcade.draw_text(str(self.score), 0, 0, arcade.color.WHITE_SMOKE, 50)


    def on_update(self, delta_time):
        self.frogsprite_list[0].update()
        self.popsprite_list.update()
        self.candysprite_list.update()
        self.spawn_popcorn()
        self.update_timer()
        self.spawn_candy()


    def spawn_popcorn(self):
        if self.timer % 100 == 0:
            self.popcorn_counter += 1
            self.popsprite_list.append(Popcorn())
            self.popsprite_list[self.popcorn_counter].center_x = randint(0,WINDOW_WIDTH)


    def spawn_candy(self):
        if self.timer % 300 == 0:
            self.candy_counter += 1
            self.candysprite_list.append(CandyFall())
            self.candysprite_list[self.candy_counter].center_x = randint(0,WINDOW_WIDTH)


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
        copy_of_popcorn = self.popsprite_list[:]
        copy_of_candy = self.candysprite_list[:]
        for popcorn in copy_of_popcorn:
            if popcorn.collides_with_point([x, y]):
                popcorn.remove_from_sprite_lists()
                arcade.play_sound(MUNCH_SOUND)
                self.popcorn_counter -= 1
                self.score += 1
        for candy in copy_of_candy:
            if candy.collides_with_point([x, y]):
                candy.remove_from_sprite_lists()
                self.candy_counter -= 1
                self.score -= 1



def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()