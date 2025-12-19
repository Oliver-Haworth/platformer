# --- MAIN.PY ---
# --- SETUP ---
import os
import pygame
from settings import *
from tilemap import Tilemap
from player import Player

# Define Asset Paths
dirt_path = os.path.join(BASE_DIR, "Assets", "Dirt.png")
grass_path = os.path.join(BASE_DIR, "Assets", "Grass.png")
character_file = os.path.join(BASE_DIR, "Assets", "character.png")

level_file = os.path.join(BASE_DIR, "levels", "level1.txt")
tile_configs = {
    '1': dirt_path,
    '2': grass_path
}

# ---  PYGAME INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_TITLE)

player = Player(100, 100, character_file)
level = Tilemap(level_file, tile_configs, 16)

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Player
    player.update() 

    # Drawing (The "Visual" Phase)
    display.fill((30, 30, 30))
    
    level.draw(display)
    player.draw(display)
    
    # Scaling (The "Output" Phase)
    scaled_surface = pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(FPS)
    print (clock)

pygame.quit()