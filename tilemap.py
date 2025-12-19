# --- tilemap.py ---
import pygame

class Tilemap:
    def __init__(self, filename, tile_configs, tile_size):
        """
        Initializes the Tilemap by loading tile images and parsing the level file.
        """
        self.tile_size = tile_size
        self.tiles = [] 
        
        # Load tile images based on the provided configurations
        self.tile_images = {}
        for char, path in tile_configs.items():
            raw_img = pygame.image.load(path).convert_alpha()
            self.tile_images[char] = pygame.transform.scale(raw_img, (tile_size, tile_size))

        # Parse the level file
        try:
            with open(filename, 'r') as f:
                rows = f.read().splitlines()
        except FileNotFoundError:
            print(f"Error: Could not find level file at {filename}")
            rows = []

        # Create tiles based on the level file
        for row_index, row_string in enumerate(rows):
            for col_index, character in enumerate(row_string):
                # Check if the character exists in our config
                if character in self.tile_images:
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    tile_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    
                    # Store both the specific image and the rect
                    self.tiles.append((self.tile_images[character], tile_rect))
        
    def draw(self, surface):
        for img, rect in self.tiles:
            surface.blit(img, rect)