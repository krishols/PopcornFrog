import arcade
from CONSTANTS import *
from Frog import FrogBody
from Popcorn import Popcorn
from random import randint
from Candy import CandyFall
from Hand import HandBoss
from Table import Table
from platform_tile import platform_tile
from filling_popcorn import RisingPopcorn
import arcade.key


class MovieTheaterFrog(arcade.Window):
    def __init__(self, x=0, y=0):
        # Initialize variables
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
        self.tile2 = None
        self.tile3 = None
        self.score = 0
        self.candysprite_list = None
        self.candy_counter = 0
        self.off_counter = 0
        self.tablesprite_list = None
        self.tilesprite_list = None
        self.rising_popcorn = None
        self.popcorn_missed_bar = 500
        self.progress_end = 0
        self.level = 1
        self.hand1_counter = 0
        self.hand2_counter = 0
        self.end_game = False
        self.lost_game = False
        self.won_game = False
        self.PhysicsEngine = None
        self.PhysicsEngine2 = None
        self.up_status = False
        self.allow_jump = False
        self.instructions = []
        self.instructions.append(INSTRUCTION_SCREEN)

        self.current_state = INSTRUCTION_PAGE

    def setup(self):
        # Setup the game (or reset the game)
        arcade.set_background_color(BACKGROUND_COLOR)
        self.frogsprite_list = arcade.SpriteList()
        self.popsprite_list = arcade.SpriteList()
        self.candysprite_list = arcade.SpriteList()
        self.handsprite_list = arcade.SpriteList()
        self.tablesprite_list = arcade.SpriteList()
        self.tilesprite_list = arcade.SpriteList()
        self.rising_popcorn = arcade.SpriteList()
        self.candysprite_list.append(CandyFall())
        self.frogsprite_list.append(FrogBody())
        self.popsprite_list.append(Popcorn())
        self.handsprite_list.append(HandBoss())
        self.handsprite_list.append(HandBoss())
        self.tablesprite_list.append(Table())
        self.tablesprite_list.append(Table())
        self.tablesprite_list.append(Table())
        self.tablesprite_list.append(Table())
        self.body = self.frogsprite_list[0]
        self.hand1 = self.handsprite_list[0]
        self.hand2 = self.handsprite_list[1]
        self.floor1 = self.tablesprite_list[0]
        self.floor1.center_x = 100
        self.floor2 = self.tablesprite_list[1]
        self.floor2.center_x = 250
        self.floor3 = self.tablesprite_list[2]
        self.floor3.center_x = 400
        self.level = 10
        self.hand1_counter = 0
        self.PhysicsEngine = arcade.PhysicsEnginePlatformer(self.body, platforms=self.tablesprite_list,
                                                            gravity_constant=GRAVITY)
        self.allow_jump = True

    def draw_instructions_page(self, page_number):
        # Draw an instruction page. Load the page as an image.
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                          page_texture.width,
                                          page_texture.height, page_texture, 0)

    def on_draw(self):
        # Render the screen

            arcade.start_render()

            if self.current_state == INSTRUCTION_PAGE:
                self.draw_instructions_page(0)

            elif self.current_state == GAME_RUNNING:
                self.draw_game()


    def draw_game(self):
        # Called when it is time to draw the world
        arcade.start_render()
        if not self.end_game:
            self.draw_game_elements()
        elif self.end_game:
            self.draw_lose_game()
        if self.won_game:
            arcade.draw_text("You won!", start_x=150, start_y=250, color=arcade.color.WHITE_SMOKE, font_size=25)

    def on_update(self, delta_time):
        # update functions
        if self.progress_end == 500:
            self.progress_level()
        self.frogsprite_list[0].update()
        self.popsprite_list.update()
        if self.level in CANDY_LEVELS:
            self.candysprite_list.update()
        if self.level in BOSS_BATTLES:
            self.hand_boss()
            if self.level == FINAL_BATTLE:
                self.hand_final()
        self.spawn_popcorn()
        self.update_timer()
        self.spawn_candy()
        self.off_screen_counter()
        self.on_draw()
        self.hand_collisions()
        self.PhysicsEngine.update()
        self.control_rising_popcorn()
        self.rising_pop_collisions()
        self.check_candy_pop_collision()


    def progress_level(self):
        # progresses  to next level when current level is completed
        self.level += 1
        self.progress_end = 0
        self.popcorn_missed_bar = 500

    def hand_boss(self):
        # directs hand chasing frog
        self.handsprite_list[0].update()
        self.hand_movement()
        self.hand1_reset()

    def hand_final(self):
        # directs hand in final boss
        self.handsprite_list[1].update()
        self.hand_movement()
        self.hand2_reset()


    def draw_game_elements(self):
        # draw basic game elements
        self.draw_instructions()
        self.floor1.draw()
        self.floor2.draw()
        self.floor3.draw()
        self.frogsprite_list.draw()
        arcade.draw_line(*self.body.tongue_args)
        self.popsprite_list.draw()
        self.draw_rising_levels()
        self.draw_candy_levels()
        self.draw_boss_levels()

    def draw_rising_levels(self):
        # draw rising popcorn and tiles
        if self.level in RISING_POP_LEVELS:
            self.tilesprite_list.draw()
            self.rising_popcorn.draw()

    def draw_candy_levels(self):
        # draw candy sprites
        if self.level in CANDY_LEVELS:
            self.candysprite_list.draw()

    def draw_boss_levels(self):
        # draw hand trying to capture frog
        if self.level in BOSS_BATTLES:
            self.hand1.draw()
            if self.level == FINAL_BATTLE:
                self.hand2.draw()
        arcade.draw_line(start_x=490, start_y=10, end_x=490, end_y=self.popcorn_missed_bar, line_width=10,
                         color=arcade.color.YELLOW)
        arcade.draw_line(start_x=10, start_y=10, end_x=10, end_y=self.progress_end, line_width=10,
                         color=[50, 205, 50])

    def draw_lose_game(self):
        # draw lose game screen
        if self.lost_game:
            arcade.draw_text("Game over! \n Click the mouse \n to try again.", start_x=150, start_y=250, color=arcade.color.WHITE_SMOKE, font_size=25, align="center")

    def control_rising_popcorn(self):
        # Creates platforms for frogs to jump on
        if self.level in RISING_POP_LEVELS:
            self.spawn_tiles()
        elif self.level not in RISING_POP_LEVELS:
            self.PhysicsEngine2 = None
        if self.level == 4:
            self.level_4_pop()
        if self.level == 7:
            self.level_7_pop()
        if self.level == 10:
            self.level_10_pop()

    def spawn_tiles(self):
        # draws tiles for rising popcorn levels
        if len(self.rising_popcorn) == 0:
            self.tilesprite_list.append(platform_tile())
            self.tilesprite_list.append(platform_tile())
            self.tile1 = self.tilesprite_list[0]
            self.tile1.center_x = 100
            self.tile1.center_y = 200
            self.tile2 = self.tilesprite_list[1]
            self.tile2.center_x = 400
            self.tile2.center_y = 200
            self.PhysicsEngine2 = arcade.PhysicsEnginePlatformer(self.body, platforms=self.tilesprite_list,
                                                                 gravity_constant=GRAVITY)
            self.PhysicsEngine2.update()
            self.rising_popcorn.append(RisingPopcorn())

    def level_4_pop(self):
        # directs rising popcorn in level 4
        if self.rising_popcorn[0].center_y <= -10:
            self.rising_popcorn[0].update()
            self.PhysicsEngine2.update()

    def level_7_pop(self):
        # directs rising popcorn in level 7
        if self.rising_popcorn[0].center_y <= -10:
            self.rising_popcorn[0].change_y = 1.5
            self.rising_popcorn[0].update()
            self.PhysicsEngine2.update()

    def level_10_pop(self):
        # directs level 10
        self.tilesprite_list.append(platform_tile())
        self.tile3 = self.tilesprite_list[2]
        self.tile3.center_x = 250
        self.tile3.center_y = 350
        self.PhysicsEngine2.update()
        if self.rising_popcorn[0].center_y <= 250:
            self.level_10_rising()
        if self.body.center_y > 500:
            self.level_10_win_game()

    def level_10_rising(self):
        # directs rising popcorn in level 10
        self.rising_popcorn[0].change_y = 1.5
        self.rising_popcorn[0].update()
        self.PhysicsEngine2.update()

    def level_10_win_game(self):
        # changes game status to won
        self.end_game = True
        self.won_game = True

    def check_candy_pop_collision(self):
        # checks and prevents candy and popcorn from colliding on top of one another
        for popcorn in self.popsprite_list:
            if popcorn.collides_with_list(self.candysprite_list):
                popcorn.center_y += 50

    def spawn_popcorn(self):
        # Creates randomly generated popcorn to fall on the screen
        if self.level in FALLING_POP_LEVELS:
            if self.timer % 100 == 0:
                self.edit_pop_list()

    def edit_pop_list(self):
        # adds popcorn sprites to list to be spawned
        self.popcorn_counter += 1
        self.popsprite_list.append(Popcorn())
        self.popsprite_list[self.popcorn_counter].center_x = randint(50, 450)
        if self.level in FASTER_FALL:
            self.popsprite_list[self.popcorn_counter].change_y = 3

    def draw_instructions(self):
        # Draws instructions for the game
        if self.level == 1:
            arcade.draw_text(
                "You are a frog trapped in a movie theatre \n popcorn machine. Eat popcorn to fill the frog's \n hunger bar! \n If you miss a popcorn your health bar goes down.",
                start_x=75, start_y=325, color=arcade.color.WHITE_SMOKE, font_size=12, width=0, align="center")
        elif self.level == 2:
            arcade.draw_text("Don't eat the candy, you'll lose hunger points!", start_x=125, start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 3:
            arcade.draw_text("The movie theatre attendant is trying to catch you! \n Dodge their hand!", start_x=125,
                             start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 4:
            arcade.draw_text(
                "They're filling up the machine! \n Jump away from the rising popcorn!\n Don't forget to keep eating falling popcorn.",
                start_x=125, start_y=325,
                color=arcade.color.WHITE_SMOKE, font_size=12,
                width=0, align="center")
        elif self.level == 5:
            arcade.draw_text("They're speeding up the machine...\n Keep eating!", start_x=125,
                             start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 6:
            arcade.draw_text("They're trying to catch you again!", start_x=125,
                             start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 7 or self.level == 8:
            arcade.draw_text("Keep eating!", start_x=125,
                             start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 9:
            arcade.draw_text("They won't give up... \n They're still trying to catch you!", start_x=125,
                             start_y=325,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")
        elif self.level == 10:
            arcade.draw_text("They're filling up the machine all the way! \n Jump out of the machine to freedom!",
                             start_x=125,
                             start_y=250,
                             color=arcade.color.WHITE_SMOKE, font_size=12,
                             width=0, align="center")

    def spawn_candy(self):
        # Spawns candy to randomly fall from the top of the screen
        if self.level in CANDY_LEVELS and self.level not in MORE_CANDY:
            self.not_more_candy()
        elif self.level in CANDY_LEVELS and self.level in MORE_CANDY:
            self.more_candy()

    def not_more_candy(self):
        # spawns candy for levels not requiring more candy
        if self.timer % 300 == 0:
            self.candy_counter += 1
            self.candysprite_list.append(CandyFall())
            self.candysprite_list[self.candy_counter].center_x = randint(50, 450)
            if self.level in FASTER_FALL:
                self.candysprite_list[self.candy_counter].change_y = 3

    def more_candy(self):
        # spawns candy for levels requiring more candy
        if self.timer % 150 == 0:
            self.candy_counter += 1
            self.candysprite_list.append(CandyFall())
            self.candysprite_list[self.candy_counter].center_x = randint(50, 450)
            if self.level in FASTER_FALL:
                self.candysprite_list[self.candy_counter].change_y = 3

    def update_timer(self):
        # Updates timer and resets when timer hits max
        if self.timer < TIMER_MAX:
            self.timer += 1
        else:
            self.timer = 1

    def off_screen_calculator(self):
        # Counts the amount of popcorn that fall off screen
        self.off_counter += 1
        self.popcorn_counter -= 1

    def popcorn_missed_game_end(self):
        """Ends game if enough popcorn falls off screen"""
        if self.popcorn_missed_bar == 0:
            self.end_game = True
            self.lost_game = True

    def off_screen_counter(self):
        """Tracks the amount of popcorn the falls off screen"""
        copy_of_counter = self.popsprite_list[:]
        for popcorn in copy_of_counter:
            if popcorn.off_screen_test():
                self.off_screen_calculator()
                popcorn.remove_from_sprite_lists()
                if self.level in EAT_5:
                    self.eat_5()
                elif self.level in EAT_10:
                    self.eat_10()

    def eat_5(self):
        # grows progress bar when level requires eating 5 popcorn
        self.popcorn_missed_bar -= (500 * (1 / 5))
        self.popcorn_missed_game_end()

    def eat_10(self):
        # grows progress bar when level requires eating 10 popcorn
        self.popcorn_missed_bar -= (500 * (1 / 3))
        self.popcorn_missed_game_end()

    def hand_movement(self):
        # Moves hand depending on player location
        if self.level in BOSS_BATTLES:
            if self.hand1.center_y >= WINDOW_HEIGHT / 2:
                self.hand_boss_battles()
            if self.level == MIDDLE_BATTLE and self.hand1.center_y < WINDOW_HEIGHT / 2:
                self.hand1.change_y = 5
            if self.level == FINAL_BATTLE and self.hand1.center_y < WINDOW_HEIGHT / 2:
                self.hand1.change_y = 5
            if self.level == FINAL_BATTLE:
                self.hand_final_battle()

    def hand_boss_battles(self):
        # moves hand in boss battle
        if self.hand1.center_x < self.body.center_x:
            self.hand1.move_right()
        elif self.hand1.center_x > self.body.center_x:
            self.hand1.move_left()

    def hand_final_battle(self):
        # moves hand in final battle
        if self.hand2.center_y >= WINDOW_HEIGHT * (3 / 4):
            if self.hand2.center_x < self.body.center_x:
                self.hand2.move_right()
            elif self.hand2.center_x > self.body.center_x:
                self.hand2.move_left()
        else:
            self.hand2.change_y = 5

    def hand1_reset(self):
        # Resets hand 1 when it reaches the bottom of the screen and tracks amount of times
        if self.hand1.center_y <= 0:
            if self.hand1_counter == 2:
                self.level += 1
                self.hand1_counter = 0
            else:
                self.hand1_counter += 1
                self.hand1.center_y = WINDOW_HEIGHT
                self.hand1.change_y = 1

    def hand2_reset(self):
        # Resets hand 2 when it reaches the bottom of the screen
        if self.hand2.center_y <= 0:
            self.hand2.center_y = WINDOW_HEIGHT

    def hand_collisions(self):
        # Checks for collision between frog and hands
        if self.level in BOSS_BATTLES:
            for hand in self.handsprite_list:
                if hand.collides_with_sprite(self.body):
                    self.end_game = True
                    self.lost_game = True

    def rising_pop_collisions(self):
        # Checks for collisions between rising popcorn and frog
        if self.level in RISING_POP_LEVELS:
            for popcorn in self.rising_popcorn:
                if popcorn.collides_with_sprite(self.body):
                    self.end_game = True
                    self.lost_game = True

    def on_key_press(self, symbol: int, modifiers: int):
        # Moves frog left and right and jumps
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.frogsprite_list[0].change_x = MOVEMENT_SPEED
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.frogsprite_list[0].change_x = -MOVEMENT_SPEED
        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            if self.PhysicsEngine.can_jump() or self.PhysicsEngine2.can_jump():
                self.body.change_y = 15

    def on_key_release(self, symbol: int, modifiers: int):
        # Stops frog from movements
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.body.change_x = 0
        elif symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.body.change_x = 0
        elif symbol == arcade.key.W or symbol == arcade.key.UP:
            self.body.change_y = 0

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Tracks mouse movement and controls frog tongue
        self.body.tongue_end_x = x
        self.body.tongue_end_y = y
        copy_of_popcorn = self.popsprite_list[:]
        for popcorn in copy_of_popcorn:
            if popcorn.collides_with_point([x, y]):
                popcorn.remove_from_sprite_lists()
                arcade.play_sound(MUNCH_SOUND)
                self.popcorn_counter -= 1
                self.score += 1
                if self.level in EAT_5:
                    self.progress_end += 100
                elif self.level in EAT_10:
                    self.progress_end += 50
        copy_of_candy = self.candysprite_list[:]
        for candy in copy_of_candy:
            if candy.collides_with_point([x, y]):
                candy.remove_from_sprite_lists()
                arcade.play_sound(YUCK_SOUND)
                self.candy_counter -= 1
                self.score -= 1
                if self.level in EAT_5:
                    self.progress_end -= 100
                elif self.level in EAT_10:
                    self.progress_end -= 50

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.current_state == INSTRUCTION_PAGE:
            self.current_state = GAME_RUNNING
        if self.current_state == END_GAME:
            self.setup()
            self.current_state = GAME_RUNNING



def main():
    window = MovieTheaterFrog()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
