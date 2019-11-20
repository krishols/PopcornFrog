import arcade
from CONSTANTS import *
from Frog import FrogBody
from Popcorn import Popcorn
from random import randint
from Candy import CandyFall
from Hand import HandBoss
import arcade.key



class MovieTheaterFrog(arcade.Window, FrogBody):
    def __init__(self, x=0, y=0):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None
        self.popsprite_list = None
        self.handsprite_list = None
        self.body = None
        self.hand1 = None
        self.timer = 1
        self.popcorn_counter = 0
        self.score = 0
        self.popcorn = []
        self.tongue_end_x = x
        self.tongue_end_y = y
        self.score = 0
        self.candysprite_list = None
        self.candy_counter = 0
        self.off_counter = 0
        self.progress_end = 0
        self.level = 1

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.popsprite_list = arcade.SpriteList()
        self.candysprite_list = arcade.SpriteList()
        self.handsprite_list = arcade.SpriteList()
        self.candysprite_list.append(CandyFall())
        self.frogsprite_list.append(FrogBody())
        self.popsprite_list.append(Popcorn())
        self.handsprite_list.append(HandBoss())
        self.body = self.frogsprite_list[0]
        self.hand1 = self.handsprite_list[0]

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.frogsprite_list.draw()
        arcade.draw_line(*self.body.tongue_args)
        self.popsprite_list.draw()
        self.candysprite_list.draw()
        if self.level == 3 or self.level == 6:
            self.handsprite_list.draw()
        arcade.draw_text(str(self.score), 0, 0, arcade.color.WHITE_SMOKE, 50)
        arcade.draw_line(start_x=10,start_y=10,end_x=10,end_y=self.progress_end, line_width=10, color= [50,205,50])

    def on_update(self, delta_time):
        self.frogsprite_list[0].update()
        self.popsprite_list.update()
        self.candysprite_list.update()
        if self.level == 3 or self.level == 6:
            self.handsprite_list[0].update()
            self.hand_movement()
        self.spawn_popcorn()
        self.update_timer()
        self.spawn_candy()
        self.off_screen_counter()
        self.progress_bar()
        self.on_draw()


    def spawn_popcorn(self):
        if self.level == 1 or self.level == 2:
            if self.timer % 100 == 0:
                self.popcorn_counter += 1
                self.popsprite_list.append(Popcorn())
                self.popsprite_list[self.popcorn_counter].center_x = randint(0,WINDOW_WIDTH)

    def spawn_candy(self):
        if self.level == 2:
            if self.timer % 300 == 0:
                self.candy_counter += 1
                self.candysprite_list.append(CandyFall())
                self.candysprite_list[self.candy_counter].center_x = randint(0,WINDOW_WIDTH)

    def update_timer(self):
        if self.timer < TIMER_MAX:
            self.timer += 1
        else:
            self.timer = 1

    def off_screen_counter(self):
        copy_of_counter = self.popsprite_list[:]
        for popcorn in copy_of_counter:
            if popcorn.off_screen_test():
                self.off_counter += 1
                popcorn.remove_from_sprite_lists()
                self.popcorn_counter -= 1


    def progress_bar(self):
        if self.level == 1:
            if self.score == 1:
                self.progress_end = 100
            elif self.score == 2:
                self.progress_end = 200
            elif self.score == 3:
                self.progress_end = 300
            elif self.score == 4:
                self.progress_end = 400
            elif self.score == 5:
                self.progress_end = 500
                self.level = 2
                self.progress_end = 0
                self.score = 0
        if self.level == 2:
            if self.score == 1:
                self.progress_end = 50
            elif self.score == 2:
                self.progress_end = 100
            elif self.score == 3:
                self.progress_end = 150
            elif self.score == 4:
                self.progress_end = 200
            elif self.score == 5:
                self.progress_end = 250
            elif self.score == 6:
                self.progress_end = 300
            elif self.score == 7:
                self.progress_end = 350
            elif self.score == 8:
                self.progress_end = 400
            elif self.score == 9:
                self.progress_end = 450
            elif self.score == 10:
                self.progress_end = 500
                self.level = 3

    def hand_movement(self):
        if self.level == 3 or self.level == 6:
            if self.hand1.center_y >= WINDOW_HEIGHT/2:
                if self.hand1.center_x < self.body.center_x:
                    self.hand1.move_right()
                elif self.hand1.center_x > self.body.center_x:
                    self.hand1.move_left()
            if self.level == 6 and self.hand1.center_y < WINDOW_HEIGHT/2:
                self.hand1.change_y = 5






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
                arcade.play_sound(YUCK_SOUND)
                self.candy_counter -= 1
                self.score -= 1



def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()