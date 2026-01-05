# --- PLAYER.PY ---
import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        try:
            self.image = pygame.transform.scale(pygame.image.load(PLAYER_IMG).convert_alpha(), (16, 16))
        except:
            self.image = pygame.Surface((16, 16))
            self.image.fill("red")
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False

        # Health Stats
        self.max_health = MAX_HEALTH
        self.current_health = STARTING_HEALTH

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False

    def check_collisions(self, tiles, axis):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if axis == 'x':
                    if self.vel.x > 0: self.rect.right = tile.rect.left
                    if self.vel.x < 0: self.rect.left = tile.rect.right
                
                if axis == 'y':
                    if self.vel.y > 0: 
                        self.rect.bottom = tile.rect.top
                        self.on_ground = True
                    elif self.vel.y < 0: 
                        self.rect.top = tile.rect.bottom
                    self.vel.y = 0
        
        if axis == 'x': self.pos.x = self.rect.x
        if axis == 'y': self.pos.y = self.rect.y

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0: self.current_health = 0

    def constrain_to_window(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
        elif self.rect.right > GAME_WIDTH:
            self.rect.right = GAME_WIDTH
            self.pos.x = self.rect.x

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.y
            self.vel.y = 0
        elif self.rect.bottom > GAME_HEIGHT:
            self.rect.bottom = GAME_HEIGHT
            self.pos.y = self.rect.y
            self.on_ground = True
            self.vel.y = 0

    def update(self, dt, tiles):
        self.get_input()
        self.vel.y += GRAVITY * dt
        
        # X movement/collision
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        self.check_collisions(tiles, 'x')
        
        # Y movement/collision
        self.on_ground = False 
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        self.check_collisions(tiles, 'y')

        self.constrain_to_window()

    def draw(self, surface):
        surface.blit(self.image, self.rect)