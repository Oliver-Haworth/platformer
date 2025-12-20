import os
import pygame
from settings import *
from tilemap import Tilemap
from player import Player

# Paths
dirt_path = os.path.join(BASE_DIR, "Assets", "Dirt.png")
grass_path = os.path.join(BASE_DIR, "Assets", "Grass.png")
character_file = os.path.join(BASE_DIR, "Assets", "character.png")
dirt_sandwiched_path = os.path.join(BASE_DIR, "Assets", "Dirt_sandwitched.png")
level_file = os.path.join(BASE_DIR, "levels", "level1.txt")

tile_configs = {
    '1': dirt_path,
    '2': grass_path,
    '1s': dirt_sandwiched_path
}

# Init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_TITLE)

player = Player(200, 300, character_file)
level = Tilemap(level_file, tile_configs, TILE_SIZE)

running = True
while running:
    # DT calculation (seconds)
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic
    player.update(level.tiles, dt)

    # Rendering
    display.fill((30, 30, 30))
    level.draw(display)
    player.draw(display)
    
    # Scale internal display to window size
    scaled_surface = pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    
    pygame.display.flip()

pygame.quit()