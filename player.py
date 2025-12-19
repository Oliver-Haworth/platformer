# --- player.py ---
import pygame
from settings import *

class Player:
    def __init__(self, x, y, character_file):
        self.image = pygame.image.load(character_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # Vertical movement 
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0


    def update(self):
        self.get_input()

        dt = 1 / FPS

        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        self.rect.topleft = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)