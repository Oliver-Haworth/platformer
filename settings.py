'''
this file is a modified version of this file:
https://github.com/Jamswert/Platformer-Learning/blob/main/config/config.py
original author: Jamswert
modified author: Oliver Haworth
'''
# --- SETTINGS.PY ---
import pygame
import os
pygame.font.init()

# INTERNAL RESOLUTION
# Internal "Game" resolution (what you code for)
GAME_WIDTH = 640
GAME_HEIGHT = 320

# How much to blow up the window
SCALING_FACTOR = 3 

# The actual window size
WINDOW_WIDTH = GAME_WIDTH * SCALING_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALING_FACTOR
WINDOW_TITLE = "Platformer"
FPS = 60

# FONTS
DEBUG_FONT = pygame.font.Font(None, size=24)


# VALUES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_SPEED = 300
PLAYER_LIVES = 3
PLAYER_HEIGHT = 36
PLAYER_WIDTH = 36
TILE_SIZE = 16
GRAVITY = 900
JUMP_STRENGTH = -400
PLAYER_JUMP_COUNT = 2

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BG_COLOR = (129, 141, 179)
