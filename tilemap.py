import pygame

class Tilemap:
    # Add 'image_path' as a new parameter
    def __init__(self, filename, image_path, tile_size):
        self.tile_size = tile_size
        # Load the ACTUAL image file here
        self.image = pygame.image.load(image_path).convert()
        self.tiles = []
        
        with open(filename, 'r') as file:
            rows = file.read().splitlines()
        
        for row_index, row_string in enumerate(rows):
            for col_index, character in enumerate(row_string):
                if character == '1':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    self.tiles.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
