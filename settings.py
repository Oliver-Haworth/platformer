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
GAME_WIDTH = 640
GAME_HEIGHT = 320

# SCALING
SCALING_FACTOR = 2
WINDOW_WIDTH = GAME_WIDTH * SCALING_FACTOR
WINDOW_HEIGHT = GAME_HEIGHT * SCALING_FACTOR
WINDOW_TITLE = "Platformer"
FPS = 60

# PHYSICS VALUES
PLAYER_SPEED = 100
GRAVITY = 2500
JUMP_STRENGTH = -550
TILE_SIZE = 16

# DIRECTORIES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
dirt_path = os.path.join(BASE_DIR, "Assets", "Dirt.png")
grass_p = os.path.join(BASE_DIR, "Assets", "Grass.png") # Updated variable name
character_file = os.path.join(BASE_DIR, "Assets", "character.png")
dirt_sandwiched_path = os.path.join(BASE_DIR, "Assets", "Dirt_sandwitched.png")
mushroom_file = os.path.join(BASE_DIR, "Assets", "mushroom.png")

level_file = os.path.join(BASE_DIR, "levels", "level1.txt")

# Updated dictionary mapping
tile_configs = {
    '1': dirt_path,
    '1g': grass_p,      
    '1s': dirt_sandwiched_path,
    '2': mushroom_file
}