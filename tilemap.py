# --- TIELMAP.PY ---
import pygame
import random
import os
from settings import *

class Tile:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Tilemap:
    def __init__(self):
        self.collidables = [] 
        self.overlays = []    
        self.load_images()
        self.build_map()

    def load_images(self):
        def load_tile(path):
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            # Fallback surface if image missing
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((100, 100, 100))
            return surf

        self.grass_surf = load_tile(GRASS_IMG)
        self.panel_surfs = [load_tile(p) for p in PANEL_IMGS]

    def build_map(self):
        if not os.path.exists(LEVEL_PATH): 
            print(f"Error: Level file not found at {LEVEL_PATH}")
            return

        with open(LEVEL_PATH, 'r') as f:
            grid = [list(line) for line in f.read().splitlines()]

        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char == '1':
                    x, y = c * TILE_SIZE, r * TILE_SIZE
                    
                    # Check for air above (handling grid boundaries)
                    air_above = True
                    if r > 0 and c < len(grid[r-1]):
                        if grid[r-1][c] == '1':
                            air_above = False

                    panel_img = random.choice(self.panel_surfs)
                    self.collidables.append(Tile(panel_img, x, y))

                    if air_above:
                        self.overlays.append(Tile(self.grass_surf, x, y))

    def draw(self, surface):
        for tile in self.collidables: surface.blit(tile.image, tile.rect)
        for deco in self.overlays: surface.blit(deco.image, deco.rect)