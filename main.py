# --- MAIN.PY ---
import os
import pygame
from settings import *
from tilemap import Tilemap

# 1. Paths and Configs (Data only)
dirt_path = os.path.join(BASE_DIR, "Assets", "Dirt.png")
grass_path = os.path.join(BASE_DIR, "Assets", "Grass.png")
level_file = os.path.join(BASE_DIR, "levels", "level1.txt")

tile_configs = {
    '1': dirt_path,
    '2': grass_path
}

# 2. Pygame Setup (MUST happen before loading/converting images)
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_TITLE)

# 3. Create the Level (Now that the display exists, convert_alpha() will work)
level = Tilemap(level_file, tile_configs, 16)

# 4. Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill((30, 30, 30))
    
    # Draw level to the small display
    level.draw(display)
    
    # Scale and Blit to the actual window
    scaled_surface = pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()