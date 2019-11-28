import arcade
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Popcorn Frog"
GAME_SPEED = 1/60
GRAVITY = 5
UP_SPEED = 5
POPCORN = arcade.load_texture("images/PopcornDraw.png", scale = .0625)
FROG = arcade.load_texture("images/cutepixelfrog_16x16.gif", scale = 3)
CANDY = arcade.load_texture("images/blob.png", scale = .1)
HAND = arcade.load_texture("images/hand.png")
TABLE = arcade.load_texture("images/table.png", scale=2)
PLATFORM_TILE = arcade.load_texture("images/platform tile.png", scale = .3)
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