import arcade
from CONSTANTS import *
from Frog import FrogBody
from Popcorn import Popcorn
from random import randint
from Candy import CandyFall
from Hand import HandBoss
from Table import Table
from platform_tile import platform_tile
import arcade.key


class MovieTheaterFrog(arcade.Window):
    def __init__(self, x=0, y=0):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.frogsprite_list = None
        self.popsprite_list = None
        self.handsprite_list = None
        self.body = None
        self.hand1 = None
        self.hand2 = None
        self.floor1 = None
        self.floor2 = None
        self.floor3 = None
        self.timer = 1
        self.popcorn_counter = 0
        self.score = 0
        self.popcorn = []
        self.tongue_end_x = x
        self.tongue_end_y = y
        self.tile1 = None
        self.score = 0
        self.candysprite_list = None
        self.candy_counter = 0
        self.off_counter = 0
        self.tablesprite_list = None
        self.tilesprite_list = None
        self.popcorn_missed_bar = 500
        self.progress_end = 0
        self.level = 1
        self.hand1_counter = 0
        self.hand2_counter = 0
        self.end_game = False
        self.PhysicsEngine = None
        self.up_status = False
        self.allow_jump = True

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.popsprite_list = arcade.SpriteList()
        self.candysprite_list = arcade.SpriteList()
        self.handsprite_list = arcade.SpriteList()
        self.tablesprite_list = arcade.SpriteList()
        self.tilesprite_list = arcade.SpriteList()
        self.candysprite_list.append(CandyFall())
        self.frogsprite_list.append(FrogBody())
        self.popsprite_list.append(Popcorn())
        self.handsprite_list.append(HandBoss())
        self.handsprite_list.append(HandBoss())
        self.tablesprite_list.append(Table())
        self.tablesprite_list.append(Table())
        self.tablesprite_list.append(Table())
        self.tilesprite_list.append(platform_tile())
        self.tilesprite_list.append(platform_tile())
        self.tilesprite_list.append(platform_tile())
        self.body = self.frogsprite_list[0]
        self.hand1 = self.handsprite_list[0]
        self.hand2 = self.handsprite_list[1]
        self.floor1 = self.tablesprite_list[0]
        self.floor1.center_x = 100
        self.floor2 = self.tablesprite_list[1]
        self.floor2.center_x = 250
        self.floor3 = self.tablesprite_list[2]
        self.floor3.center_x = 400
        self.tile1 = self.tilesprite_list[0]
        self.tile1.center_x = 100
        self.level = 1
        self.hand1_counter = 0
        self.PhysicsEngine = arcade.PhysicsEnginePlatformer(self.body, platforms=self.tablesprite_list or self.tilesprite_list, gravity_constant=GRAVITY)
        self.allow_jump = True

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        if not self.end_game:
            self.tablesprite_list.draw()
            self.frogsprite_list.draw()
            self.tilesprite_list.draw()
            arcade.draw_line(*self.body.tongue_args)
            self.popsprite_list.draw()
            if self.level == 2:
                self.candysprite_list.draw()
            if self.level in BOSS_BATTLES:
                self.hand1.draw()
                if self.level == FINAL_BATTLE:
                    self.hand2.draw()
            arcade.draw_line(start_x=490, start_y=10, end_x=490, end_y=self.popcorn_missed_bar, line_width=10,
                             color=arcade.color.YELLOW)
            arcade.draw_line(start_x=10, start_y=10, end_x=10, end_y=self.progress_end, line_width=10,
                             color=[50, 205, 50])
        elif self.end_game:
            arcade.draw_text("Game over!", start_x=60, start_y=250, color=arcade.color.WHITE_SMOKE, font_size=25)

    def on_update(self, delta_time):
        if self.progress_end == 500:
            self.level += 1
            self.progress_end = 0
            self.popcorn_missed_bar = 500
        self.frogsprite_list[0].update()
        self.popsprite_list.update()
        if self.level == 2:
            self.candysprite_list.update()
        if self.level in BOSS_BATTLES:
            self.handsprite_list[0].update()
            self.hand_movement()
            self.hand1_reset()
            if self.level == FINAL_BATTLE:
                self.handsprite_list[1].update()
                self.hand_movement()
                self.hand2_reset()
        self.spawn_popcorn()
        self.update_timer()
        self.spawn_candy()
        self.off_screen_counter()
        self.on_draw()
        self.hand_collisions()
        self.PhysicsEngine.update()

    def spawn_popcorn(self):
        if self.level == 1 or self.level == 2:
            if self.timer % 100 == 0:
                self.popcorn_counter += 1
                self.popsprite_list.append(Popcorn())
                self.popsprite_list[self.popcorn_counter].center_x = randint(50, 450)

    def spawn_candy(self):
        if self.level == 2:
            if self.timer % 300 == 0:
                self.candy_counter += 1
                self.candysprite_list.append(CandyFall())
                self.candysprite_list[self.candy_counter].center_x = randint(50, 450)

    def update_timer(self):
        if self.timer < TIMER_MAX:
            self.timer += 1
        else:
            self.timer = 1

    def off_screen_calculator(self):
        self.off_counter += 1
        self.popcorn_counter -= 1

    def popcorn_missed_game_end(self):
        if self.popcorn_missed_bar == 0:
            self.end_game = True

    def off_screen_counter(self):
        copy_of_counter = self.popsprite_list[:]
        for popcorn in copy_of_counter:
            if popcorn.off_screen_test():
                self.off_screen_calculator()
                popcorn.remove_from_sprite_lists()
                if self.level == 1:
                    self.popcorn_missed_bar -= (500 * (1 / 5))
                    self.popcorn_missed_game_end()
                elif self.level == 2:
                    self.popcorn_missed_bar -= (500 * (1 / 3))
                    self.popcorn_missed_game_end()

    def hand_movement(self):
        if self.level in BOSS_BATTLES:
            if self.hand1.center_y >= WINDOW_HEIGHT / 2:
                if self.hand1.center_x < self.body.center_x:
                    self.hand1.move_right()
                elif self.hand1.center_x > self.body.center_x:
                    self.hand1.move_left()
            if self.level == MIDDLE_BATTLE and self.hand1.center_y < WINDOW_HEIGHT / 2:
                self.hand1.change_y = 5
            if self.level == FINAL_BATTLE and self.hand1.center_y < WINDOW_HEIGHT / 2:
                self.hand1.change_y = 5
            if self.level == FINAL_BATTLE:
                if self.hand2.center_y >= WINDOW_HEIGHT * (3 / 4):
                    if self.hand2.center_x < self.body.center_x:
                        self.hand2.move_right()
                    elif self.hand2.center_x > self.body.center_x:
                        self.hand2.move_left()
                else:
                    self.hand2.change_y = 5

    def hand1_reset(self):
        if self.hand1.center_y <= 0:
            if self.hand1_counter == 2:
                self.level += 1
                self.hand1_counter = 0
            else:
                self.hand1_counter += 1
                self.hand1.center_y = WINDOW_HEIGHT
                self.hand1.change_y = 1

    def hand2_reset(self):
        if self.hand2.center_y <= 0:
            self.hand2.center_y = WINDOW_HEIGHT

    def hand_collisions(self):
        for hand in self.handsprite_list:
            if hand.collides_with_sprite(self.body):
                self.end_game = True

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.frogsprite_list[0].change_x = MOVEMENT_SPEED
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.frogsprite_list[0].change_x = -MOVEMENT_SPEED
        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            if self.PhysicsEngine.can_jump():
                self.body.change_y = 25

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.body.change_x = 0
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.body.change_x = 0
        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.body.change_y = 0

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
                if self.level == 1:
                    self.progress_end += 100
                elif self.level == 2:
                    self.progress_end += 50
        for candy in copy_of_candy:
            if candy.collides_with_point([x, y]):
                candy.remove_from_sprite_lists()
                arcade.play_sound(YUCK_SOUND)
                self.candy_counter -= 1
                self.score -= 1
                if self.level == 1:
                    self.progress_end -= 100
                elif self.level == 2:
                    self.progress_end -= 50


def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
