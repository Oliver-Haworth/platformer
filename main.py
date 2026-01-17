# --- main.py ---
# Import Modules
import pygame, os
from settings import Settings, Path
from tilemap import Tilemap
from player import Player
from menu import pause
from log_system import log

# Clear Logs
with open('game_log.log', 'w'):
    log.debug('main.py - new session started')

log.debug('main.py - All modules imported')

class Game:
    def __init__(self):
        # Pygame Initialization
        pygame.init()
        pygame.mixer.init()

        # Set up display
        self.screen = pygame.display.set_mode((Settings.GAME_WIDTH * Settings.window_width, Settings.GAME_HEIGHT * Settings.window_height))
        self.canvas = pygame.Surface((Settings.GAME_WIDTH, Settings.GAME_HEIGHT))
        self.clock = pygame.time.Clock()

        # Load background
        if os.path.exists(Path.BACKGROUND_IMG):
            self.bg_surf = pygame.image.load(Path.BACKGROUND_IMG).convert()
            self.bg_surf = pygame.transform.scale(self.bg_surf, (Settings.GAME_WIDTH, Settings.GAME_HEIGHT))
        else:
            log.error('main.py - background file not found - reverting to solid colour')
            self.bg_surf = pygame.Surface((Settings.GAME_WIDTH, Settings.GAME_HEIGHT))
            self.bg_surf.fill((40, 20, 60))
        log.debug('main.py - background has loaded')

        # Initialize Tilemap and Player
        self.tilemap = Tilemap()
        self.player = Player(200, 200)
        self.running = True
        log.debug('main.py - player and tilemap initialised')
     
    # UI Drawing
    def draw_ui(self):
        ratio = self.player.current_health / self.player.max_health
        bg_rect = pygame.Rect(Settings.HEALTH_BAR_X, Settings.HEALTH_BAR_Y, Settings.HEALTH_BAR_WIDTH, Settings.HEALTH_BAR_HEIGHT)
        pygame.draw.rect(self.canvas, (40, 40, 40), bg_rect)
        fg_rect = pygame.Rect(Settings.HEALTH_BAR_X, Settings.HEALTH_BAR_Y, Settings.HEALTH_BAR_WIDTH * ratio, Settings.HEALTH_BAR_HEIGHT)
        pygame.draw.rect(self.canvas, (220, 40, 40), fg_rect)
        pygame.draw.rect(self.canvas, (200, 200, 200), bg_rect, 1)

    log.debug('main.py - starting main loop')

    # Main game loop
    def run(self):
        while self.running:
            dt = self.clock.tick(Settings.fps) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.player.take_damage(10)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.player.lazer(2, self.player.pos.x, self.player.pos.y)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause(self)

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