import pygame
from log_system import log

class Button:
    def __init__(self, x, y, width, height, text, font, color=(0, 0, 0), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        
    def draw(self, surface, mouse_pos):
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(surface, current_color, self.rect)
        
        # Draw the text
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(mouse_pos)
        return False

def pause(game):
    log.debug('menu.py - game paused')
    font = pygame.font.SysFont('Arial', 24, bold=True)
    paused = True

    # 1. Instantiate buttons here
    resume_btn = Button(235, 100, 150, 50, "RESUME", font)
    quit_btn = Button(235, 175, 150, 50, "QUIT", font)
    settings = Button(235, 250, 150, 50, "settings", font)

    while paused:
        # Calculate mouse ratios
        canvas_w, canvas_h = game.canvas.get_size()
        screen_w, screen_h = game.screen.get_size()
        ratio_x, ratio_y = canvas_w / screen_w, canvas_h / screen_h
        
        raw_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (raw_mouse_pos[0] * ratio_x, raw_mouse_pos[1] * ratio_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # 2. Check for button clicks
            if resume_btn.is_clicked(mouse_pos, event):
                log.debug('menu - resume clicked!')
                paused = False
                
            if quit_btn.is_clicked(mouse_pos, event):
                log.debug('menu.py - quit clicked')
                pygame.quit()
                quit()

            if settings.is_clicked(mouse_pos, event):
                log.debug('menu.py - settings clicked')
                paused = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

        # --- DRAWING ---
        game.canvas.fill((255, 255, 255)) 
        
        # 3. Draw buttons
        resume_btn.draw(game.canvas, mouse_pos)
        quit_btn.draw(game.canvas, mouse_pos)
        settings.draw(game.canvas , mouse_pos)

        # Final Blit
        scaled_surf = pygame.transform.scale(game.canvas, (screen_w, screen_h))
        game.screen.blit(scaled_surf, (0, 0))
        pygame.display.flip()
        game.clock.tick(60)