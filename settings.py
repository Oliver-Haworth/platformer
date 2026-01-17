'''
dispite being heavly modified this file is a modified version of this file:
https://github.com/Jamswert/Platformer-Learning/blob/main/config/config.py
original author: Jamswert
modified author: Oliver-Haworth
'''
# --- settings.py ---
# Import Modules
import os
from log_system import log

class Settings():
    '''
    stores all game settings

    I hope to add a settings menu in future updates to modify some of these in-game
    '''

    # Display
    # GAME WIDTH/HIGHT defines the internal resolution the game is built for
    GAME_WIDTH, GAME_HEIGHT = 640, 320

    # Dictionary of resolution scales
    RESOLUTION_OPTIONS = {
        '640x320': (1, 1),
        '1280x640': (2, 2),
        '1920x960': (3, 3),
        '2560x1280': (4, 4),
        'fullscreen':(0, 0)
    }

    # window hight/width is the resolution of the final upscalled game
    resolution_choice = RESOLUTION_OPTIONS ['fullscreen']
    window_width, window_height = resolution_choice

    log.debug('settings.py - resolution set to ' + 'fullscreen')

    fps = 60

    # Physics
    '''
    tile size = size of tile assets (16 x 16)
    gravity = the rate the player falls down
    player speed = the speed of player movement
    jump force = the force of player jump'''
    tile_size = 16
    gravity = 2000
    player_speed = 140
    jump_force = -500
    animation_speed = 4

    # Health System
    MAX_HEALTH = 500
    STARTING_HEALTH = 500

    # UI Layout
    HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT = 150, 12
    HEALTH_BAR_X, HEALTH_BAR_Y = 15, 15

class Path():
        '''
        defines all file paths used in the game
        '''

        # Base Directories
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
        LEVELS_DIR = os.path.join(BASE_DIR, "levels")

        # Visual Asset Paths
        LEVEL_PATH = os.path.join(LEVELS_DIR, "level1.txt")
        PLAYER_IMG = os.path.join(ASSETS_DIR, "character.png")
        PLAYER_IMG2 = os.path.join(ASSETS_DIR, "character_smol.png")
        GRASS_IMG  = os.path.join(ASSETS_DIR, "Grass.png")
        BACKGROUND_IMG = os.path.join(ASSETS_DIR, "background.png")
        PANEL_IMGS = []
        for i in range(1, 4):
             PANEL_IMGS.append(os.path.join(ASSETS_DIR, f"pannel{i}.png"))
        SHARD_IMGS = [os.path.join(ASSETS_DIR, "shards.png"), os.path.join(ASSETS_DIR, "shards2.png")]

        # Audio Paths
        boing1 = os.path.join(ASSETS_DIR, "voice_1.wav")
        boing2 = os.path.join(ASSETS_DIR, "voice_2.wav")
        boing3 = os.path.join(ASSETS_DIR, "voice_3.wav")
        boing4 = os.path.join(ASSETS_DIR, "voice_4.wav")
        pew1 = os.path.join(ASSETS_DIR, "pew_1.wav")
        damage = os.path.join(ASSETS_DIR, "damage.wav")
        log.debug('settings.py - asset paths defined')