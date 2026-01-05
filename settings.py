'''
this file is a modified version of this file:
https://github.com/Jamswert/Platformer-Learning/blob/main/config/config.py
original author: Jamswert
modified author: Oliver-Haworth
'''
# --- SETTINGS.PY ---
import os

# Display
GAME_WIDTH, GAME_HEIGHT = 640, 320
WINDOW_SCALE = 3
FPS = 60

# Physics
TILE_SIZE = 16
GRAVITY = 2000
PLAYER_SPEED = 140
JUMP_FORCE = -500

# Health System
MAX_HEALTH = 100
STARTING_HEALTH = 100

# UI Layout (Internal Resolution)
HB_WIDTH = 150
HB_HEIGHT = 12
HB_X, HB_Y = 15, 15

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "Assets")
LEVELS = os.path.join(BASE_DIR, "levels")
LEVEL_PATH = os.path.join(LEVELS, "level1.txt")

PLAYER_IMG = os.path.join(ASSETS, "character.png")
GRASS_IMG  = os.path.join(ASSETS, "Grass.png")
BACKGROUND_IMG = os.path.join(ASSETS, "background.png")
PANEL_IMGS = [os.path.join(ASSETS, f"pannel{i}.png") for i in range(1, 4)]
SHARD_IMGS = [os.path.join(ASSETS, "shards.png")]