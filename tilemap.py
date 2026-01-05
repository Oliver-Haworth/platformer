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
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill((150, 150, 150))
            return surf

        self.grass_surf = load_tile(GRASS_IMG)
        self.panel_surfs = [load_tile(p) for p in PANEL_IMGS]
        self.shard_surfs = [load_tile(s) for s in SHARD_IMGS]

    def build_map(self):
        if not os.path.exists(LEVEL_PATH): 
            return

        with open(LEVEL_PATH, 'r') as f:
            grid = [list(line) for line in f.read().splitlines()]

        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                if char == '1':
                    air_above = True
                    if r > 0 and c < len(grid[r-1]):
                        if grid[r-1][c] == '1': air_above = False

                    self.collidables.append(Tile(random.choice(self.panel_surfs), x, y))
                    if air_above:
                        self.overlays.append(Tile(self.grass_surf, x, y))
                
                elif char == '2':
                    self.collidables.append(Tile(random.choice(self.shard_surfs), x, y))

    def draw(self, surface):
        for tile in self.collidables: surface.blit(tile.image, tile.rect)
        for deco in self.overlays: surface.blit(deco.image, deco.rect)