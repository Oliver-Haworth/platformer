# --- MAIN.PY ---
import pygame
import os
from settings import *
from tilemap import Tilemap
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH * WINDOW_SCALE, GAME_HEIGHT * WINDOW_SCALE))
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load background
        if os.path.exists(BACKGROUND_IMG):
            self.bg_surf = pygame.image.load(BACKGROUND_IMG).convert()
            self.bg_surf = pygame.transform.scale(self.bg_surf, (GAME_WIDTH, GAME_HEIGHT))
        else:
            self.bg_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            self.bg_surf.fill((40, 20, 60)) # Purple fallback

        self.tilemap = Tilemap()
        self.player = Player(200, 200)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False

            # Update
            self.player.update(dt, self.tilemap.collidables)

            # Draw
            self.canvas.blit(self.bg_surf, (0, 0))
            self.tilemap.draw(self.canvas)
            self.player.draw(self.canvas)

            # Display Scaling
            scaled_win = pygame.transform.scale(self.canvas, self.screen.get_size())
            self.screen.blit(scaled_win, (0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
    pygame.quit()