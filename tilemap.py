# --- TIELMAP.PY ---
import pygame

class Tilemap:
    def __init__(self, filename, tile_configs, tile_size):
        self.tile_size = tile_size
        self.tiles = [] 
        
        # Load and scale tile images
        self.tile_images = {}
        for char, path in tile_configs.items():
            raw_img = pygame.image.load(path).convert_alpha()
            self.tile_images[char] = pygame.transform.scale(raw_img, (tile_size, tile_size))

        # 1. Load the level into a 2D grid (list of lists)
        grid = []
        try:
            with open(filename, 'r') as f:
                grid = [list(line) for line in f.read().splitlines()]
        except FileNotFoundError:
            print(f"Error: Could not find level file at {filename}")
            return

        # 2. Process the grid to create tiles
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char in self.tile_images:
                    img = self.tile_images[char]
                    
                    # SANDWICH LOGIC: Check if Dirt ('1') should be Sandwiched ('1s')
                    if char == '1':
                        has_above = False
                        has_below = False

                        # Check neighbor above (Dirt or Grass)
                        if r > 0:
                            if grid[r-1][c] in ['1', '2']:
                                has_above = True
                        
                        # Check neighbor below (Dirt)
                        if r < len(grid) - 1:
                            if grid[r+1][c] == '1':
                                has_below = True

                        # If there is something above and below, swap the texture
                        if has_above and has_below:
                            img = self.tile_images.get('1s', img)

                    # Create the Rect and store the tile
                    x = c * self.tile_size
                    y = r * self.tile_size
                    tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    self.tiles.append((img, tile_rect))
        
    def draw(self, surface):
        for img, rect in self.tiles:
            surface.blit(img, rect)