# --- PLAYER.PY ---
import pygame
from settings import *

class Player:
    def __init__(self, x, y, character_file):
        try:
            self.image = pygame.image.load(character_file).convert_alpha()
            self.image = pygame.transform.scale(self.image, (16, 16))
        except:
            self.image = pygame.Surface((16, 16))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal
        if keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        elif keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        else:
            self.velocity.x = 0

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            self.on_ground = False

    def check_collisions(self, tiles, direction):
        for _, tile_rect in tiles:
            if self.rect.colliderect(tile_rect):
                if direction == 'horizontal':
                    if self.velocity.x > 0: self.rect.right = tile_rect.left
                    elif self.velocity.x < 0: self.rect.left = tile_rect.right
                    self.pos.x = self.rect.x

                if direction == 'vertical':
                    if self.velocity.y > 0: # Falling
                        self.rect.bottom = tile_rect.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0: # Head bonk
                        self.rect.top = tile_rect.bottom
                        self.velocity.y = 0
                    self.pos.y = self.rect.y

    def update(self, tiles, dt):
        self.get_input()

        # X Movement
        self.pos.x += self.velocity.x * dt
        self.rect.x = round(self.pos.x)
        self.check_collisions(tiles, 'horizontal')

        # Y Movement (Gravity)
        self.velocity.y += GRAVITY * dt
        self.pos.y += self.velocity.y * dt
        self.rect.y = round(self.pos.y)
        
        # Reset ground status before checking vertical collisions
        if self.velocity.y != 0:
            self.on_ground = False
            
        self.check_collisions(tiles, 'vertical')

        # Screen Boundaries
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
        elif self.rect.right > GAME_WIDTH:
            self.rect.right = GAME_WIDTH
            self.pos.x = self.rect.x

    def draw(self, surface):
        surface.blit(self.image, self.rect)