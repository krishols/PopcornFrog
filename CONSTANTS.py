import arcade
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Popcorn Frog"
GAME_SPEED = 1/60
FROG = arcade.load_texture("images/cutepixelfrog_16x16.gif", scale = 3)
POPCORN = arcade.load_texture("images/PopcornDraw.png", scale = .0625)
CANDY = arcade.load_texture("images/blob.png", scale = .1)
MOVEMENT_SPEED = 5
FALL_SPEED = 1
MAX_LENGTH = 100
TIMER_MAX = 300
