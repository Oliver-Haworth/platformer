# --- player.py ---
import pygame
import random
from settings import *
import time

class Player:
    def __init__(self, x, y):
        # Physics state
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        
        # --- AUDIO SETUP ---
        # Pre-load the sound objects once so the game doesn't lag when you jump
        self.jump_sounds = (
            pygame.mixer.Sound(boing1), 
            pygame.mixer.Sound(boing2), 
            pygame.mixer.Sound(boing3),
            pygame.mixer.Sound(boing4)
        )
        self.last_sound = None

        self.pew_sounds = (
            pygame.mixer.Sound(pew1),
        )

        self.last_lazer_sound = None

        # Health Stats
        self.max_health = MAX_HEALTH
        self.current_health = STARTING_HEALTH

        # Animation Settings
        self.sprites = []
        self.frame_index = 0
        self.animation_speed = 4 
        self.facing_right = True

        try:
            img1 = pygame.image.load(PLAYER_IMG).convert_alpha()
            img2 = pygame.image.load(PLAYER_IMG2).convert_alpha()
            self.sprites.append(pygame.transform.scale(img1, (16, 16)))
            self.sprites.append(pygame.transform.scale(img2, (16, 16)))
            self.image = self.sprites[0]
        except Exception as e:
            print(f"Error loading player images: {e}")
            self.image = pygame.Surface((16, 16))
            self.image.fill("red")
            self.sprites.append(self.image)
        
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        
        self.image = self.sprites[int(self.frame_index)]

        if self.vel.x > 0: self.facing_right = True
        elif self.vel.x < 0: self.facing_right = False

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = JUMP_FORCE
            
            # --- RANDOMIZATION LOGIC ---
            # Pick a sound from our pre-loaded list
            jump_sound = random.choice(self.jump_sounds)
            
            # Keep picking a new one if it matches the last sound played
            while jump_sound == self.last_sound:
                jump_sound = random.choice(self.jump_sounds)
            
            # Update the "memory" and play it
            self.last_sound = jump_sound
            jump_sound.play()
            
            self.on_ground = False

    # Handle Gun
    def pew(self, burst_shot_rate, Player_X, Player_Y):
        for shots_taken in range(burst_shot_rate):
            # Pick a random sound
            lazer_sound = random.choice(self.pew_sounds)
        
            #while lazer_sound == self.last_lazer_sound:
                #lazer_sound = random.choice(self.pew_sounds)

        #self.last_lazer_sound = lazer_sound
        lazer_sound.play()
        print(f"pew at {Player_X} {Player_Y}")

    # Check and resolve collisions
    def check_collisions(self, tiles, axis):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if axis == 'x':
                    if self.vel.x > 0: self.rect.right = tile.rect.left
                    if self.vel.x < 0: self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x
                
                if axis == 'y':
                    if self.vel.y > 0: 
                        self.rect.bottom = tile.rect.top
                        self.on_ground = True
                    elif self.vel.y < 0: 
                        self.rect.top = tile.rect.bottom
                    self.vel.y = 0
                    self.pos.y = self.rect.y

    # Handle taking damage
    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0: self.current_health = 0


    # Keep player within window bounds
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

    # Update player state
    def update(self, dt, tiles):
        self.get_input()
        self.vel.y += GRAVITY * dt
        
        # X Axis
        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        self.check_collisions(tiles, 'x')
        
        # Y Axis
        self.on_ground = False 
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        self.check_collisions(tiles, 'y')

        self.constrain_to_window()
        self.animate(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)