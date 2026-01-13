# --- tilemap.py ---
# Import Modules
import pygame, random, os
from settings import Settings, Path

# Tile Classes
class Tile:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, Settings.tile_size, Settings.tile_size)

# Animated Tile Class
class AnimatedTile(Tile):
    def __init__(self, frames, x, y, speed=3):
        super().__init__(frames[0], x, y)
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = speed

    # Update animation frame
    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

# Tilemap Class
class Tilemap:
    def __init__(self):
        self.collidables = [] 
        self.overlays = []    
        self.load_images()
        self.build_map()

    # Load tile images
    def load_images(self):
        def load_tile(path):
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (Settings.tile_size, Settings.tile_size))
            surf = pygame.Surface((Settings.tile_size, Settings.tile_size))
            surf.fill((150, 150, 150))
            return surf
        
        # Load individual tile images
        self.grass_surf = load_tile(Path.GRASS_IMG)
        self.panel_surfs = [load_tile(p) for p in Path.PANEL_IMGS]
        self.shard_surfs = [load_tile(s) for s in Path.SHARD_IMGS]

    # Build the tilemap from level file
    def build_map(self):
        if not os.path.exists(Path.LEVEL_PATH): return

        with open(Path.LEVEL_PATH, 'r') as f:
            grid = [list(line) for line in f.read().splitlines()]

        # Create tiles based on characters in the grid
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                x, y = c * Settings.tile_size, r * Settings.tile_size
                if char == '1':
                    air_above = True
                    if r > 0 and c < len(grid[r-1]):
                        if grid[r-1][c] == '1': air_above = False
                    self.collidables.append(Tile(random.choice(self.panel_surfs), x, y))
                    if air_above:
                        self.overlays.append(Tile(self.grass_surf, x, y))
                elif char == '2':
                    # Create the animated shard
                    self.collidables.append(AnimatedTile(self.shard_surfs, x, y))

    # Update animated tiles
    def update(self, dt):
        for tile in self.collidables:
            if hasattr(tile, 'update'):
                tile.update(dt)

    # Draw tiles to the surface
    def draw(self, surface):
        for tile in self.collidables: surface.blit(tile.image, tile.rect)
        for deco in self.overlays: surface.blit(deco.image, deco.rect)