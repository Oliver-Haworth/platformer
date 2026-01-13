import pygame
from settings import Settings, Path
from log_system import log

def pause(game):
    log.debug('menu.py - game paused')
    paused = True
    while paused:

        # if application closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # esc = close menue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    log.debug('menue.py - game unpaused')
                    paused = False
        # draw button
        pygame.draw.rect(game.canvas, (0, 0, 0), (50, 50, 100, 40))

        # white background
        game.canvas.fill((255, 255, 255)) 

        # 4. Update display
        scaled_size = game.screen.get_size() 
        scaled_surf = pygame.transform.scale(game.canvas, scaled_size)
        game.screen.blit(scaled_surf, (0, 0))
        pygame.display.flip()
        game.clock.tick(60)