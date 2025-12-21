# --- TIELMAP.PY ---
import pygame

class Tilemap:
    def __init__(self, filename, tile_configs, tile_size):
        self.tile_size = tile_size
        self.tiles = []      # Solid tiles
        self.mushrooms = []  # Pickups
        
        self.tile_images = {}
        for char, path in tile_configs.items():
            raw_img = pygame.image.load(path).convert_alpha()
            self.tile_images[char] = pygame.transform.scale(raw_img, (tile_size, tile_size))

        grid = []
        try:
            with open(filename, 'r') as f:
                grid = [list(line) for line in f.read().splitlines()]
        except FileNotFoundError:
            print(f"Error: Could not find level file at {filename}")
            return

        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char in self.tile_images:
                    img = self.tile_images[char]
                    x = c * self.tile_size
                    y = r * self.tile_size
                    tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

                    # Separate Mushroom logic from Solid logic
                    if char == '2':
                        self.mushrooms.append({'img': img, 'rect': tile_rect})
                    else:
                        # Apply Sandwich/Grass logic for solid dirt
                        if char == '1':
                            has_above = False
                            has_below = False
                            if r > 0 and grid[r-1][c] != ".": has_above = True
                            if r < len(grid) - 1 and grid[r+1][c] == '1': has_below = True

                            if has_above and has_below:
                                img = self.tile_images.get('1s', img)
                            if not has_above:
                                img = self.tile_images.get('1g', img)
                        
                        self.tiles.append((img, tile_rect))
        
    def draw(self, surface):
        # Draw solid tiles
        for img, rect in self.tiles:
            surface.blit(img, rect)
        
        # Draw mushrooms
        for mushroom in self.mushrooms:
            surface.blit(mushroom['img'], mushroom['rect'])