import arcade
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Popcorn Frog"
GAME_SPEED = 1/60
GRAVITY = .5
UP_SPEED = 5
POPCORN = arcade.load_texture("images/PopcornDraw.png", scale = .0625)
FROG = arcade.load_texture("images/frog sprite.png", scale = .15)
CANDY = arcade.load_texture("images/candy_sprite.png", scale = .15)
HAND = arcade.load_texture("images/hand.png")
TABLE = arcade.load_texture("images/counter_sprite.png", scale=.44)
PLATFORM_TILE = arcade.load_texture("images/tile_sprite.png", scale = .3)
MOVEMENT_SPEED = 5
FALL_SPEED = 1
MAX_LENGTH = 100
TIMER_MAX = 300
MUNCH_SOUND = arcade.load_sound("sounds/munch.wav")
YUCK_SOUND = arcade.load_sound("sounds/yuck.wav")
BOSS_BATTLES = [3,6,9]
FIRST_BATTLE = 3
MIDDLE_BATTLE = 6
FINAL_BATTLE = 9
RISING_POP_LEVELS = [4,7,10]
FALLING_POP_LEVELS = [1,2,4,5,7,8]
CANDY_LEVELS = [2,4,5,7,8]
RISE_SPEED = .5
RISING_POPCORN = arcade.load_texture("images/popcorn_fillup.png", scale = .5)
EAT_5 = [1,4,7]
EAT_10 = [2,5,8]
FASTER_FALL = [5,7,8]
FASTER_RISE = [7,10]
MORE_CANDY = [8]
INSTRUCTION_SCREEN = arcade.load_texture("images/start_screen.png")
LOSE_SCREEN = arcade.load_texture("images/lose_screen.png")
WON_SCREEN = arcade.load_texture("images/won_screen.png")
INSTRUCTION_PAGE = 1
GAME_RUNNING = 2
END_GAME = 3
WON_GAME = 4