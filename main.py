# --- MAIN.PY ---
import pygame
import os
from settings import *
from tilemap import Tilemap
from player import Player

# Main game class
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH * WINDOW_SCALE, GAME_HEIGHT * WINDOW_SCALE))
        self.canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        # Load background
        if os.path.exists(BACKGROUND_IMG):
            self.bg_surf = pygame.image.load(BACKGROUND_IMG).convert()
            self.bg_surf = pygame.transform.scale(self.bg_surf, (GAME_WIDTH, GAME_HEIGHT))
        else:
            self.bg_surf = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            self.bg_surf.fill((40, 20, 60))

        # Initialize Tilemap and Player
        self.tilemap = Tilemap()
        self.player = Player(200, 200)
        self.running = True
    
    # UI Drawing
    def draw_ui(self):
        ratio = self.player.current_health / self.player.max_health
        bg_rect = pygame.Rect(HB_X, HB_Y, HB_WIDTH, HB_HEIGHT)
        pygame.draw.rect(self.canvas, (40, 40, 40), bg_rect)
        fg_rect = pygame.Rect(HB_X, HB_Y, HB_WIDTH * ratio, HB_HEIGHT)
        pygame.draw.rect(self.canvas, (220, 40, 40), fg_rect)
        pygame.draw.rect(self.canvas, (200, 200, 200), bg_rect, 1)

    # Main game loop
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.player.take_damage(10)

            # Update Player Logic
            self.player.update(dt, self.tilemap.collidables) 
            self.tilemap.update(dt)

            # Render Logic
            self.canvas.blit(self.bg_surf, (0, 0))
            self.tilemap.draw(self.canvas)
            self.player.draw(self.canvas)
            self.draw_ui()

            # Final Upscale
            scaled_win = pygame.transform.scale(self.canvas, self.screen.get_size())
            self.screen.blit(scaled_win, (0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
    pygame.quit()