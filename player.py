# --- player.py ---
# Import Modules
import pygame, random
from settings import Settings, Path
from log_system import log

class Player:
    def __init__(self, x, y):
        '''
        Player class handles anything tied to the player character: movement, health, animations, and sound effects
        '''

        # Position and Movement
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        
        # --- AUDIO SETUP ---
        # Pre-load jump sounds
        self.jump_sounds = (
            pygame.mixer.Sound(Path.boing1), 
            pygame.mixer.Sound(Path.boing2), 
            pygame.mixer.Sound(Path.boing3),
            pygame.mixer.Sound(Path.boing4)
        )
        self.last_sound = None

        # Pre-load lazer sounds
        self.lazer_sounds = (
            pygame.mixer.Sound(Path.pew1),
        )

        self.damage_sounds = (
            pygame.mixer.Sound(Path.damage),
        )

        self.last_lazer_sound = None

        # Health Stats
        self.max_health = Settings.MAX_HEALTH
        self.current_health = Settings.STARTING_HEALTH

        # Animation Settings
        self.sprites = []
        self.frame_index = 0
        self.facing_right = True

        try:
            img1 = pygame.image.load(Path.PLAYER_IMG).convert_alpha()
            img2 = pygame.image.load(Path.PLAYER_IMG2).convert_alpha()
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
        self.frame_index += Settings.animation_speed * dt
        if self.frame_index >= len(self.sprites):
            self.frame_index = 0
        
        self.image = self.sprites[int(self.frame_index)]

        if self.vel.x > 0: self.facing_right = True
        elif self.vel.x < 0: self.facing_right = False

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = (keys[pygame.K_d] - keys[pygame.K_a]) * Settings.player_speed
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = Settings.jump_force
            
            jump_sound = random.choice(self.jump_sounds)
            
            while jump_sound == self.last_sound:
                jump_sound = random.choice(self.jump_sounds)
            
            self.last_sound = jump_sound
            jump_sound.play()
            log.debug('player.py - jump - boing')
            
            self.on_ground = False

    # Handle lazer
    def lazer(self, burst_shot_rate, Player_X, Player_Y):
        for shots_taken in range(burst_shot_rate):
            # Pick a random sound
            lazer_sound = random.choice(self.lazer_sounds)
        
            #while lazer_sound == self.last_lazer_sound:
                #lazer_sound = random.choice(self.lazer_sounds)

        #self.last_lazer_sound = lazer_sound
        log.debug(f'player.py - lazer shot from {round(Player_X)}, {round(Player_Y)}')
        lazer_sound.play()

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
        damage_sound = random.choice(self.damage_sounds)
        damage_sound.play()
        log.debug(f'player.py - {amount} damage taken - {self.current_health} left')


    # Keep player within window bounds
    def constrain_to_window(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
        elif self.rect.right > Settings.GAME_WIDTH:
            self.rect.right = Settings.GAME_WIDTH
            self.pos.x = self.rect.x

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.y
            self.vel.y = 0
        elif self.rect.bottom > Settings.GAME_HEIGHT:
            self.rect.bottom = Settings.GAME_HEIGHT
            self.pos.y = self.rect.y
            self.on_ground = True
            self.vel.y = 0

    # Update player state
    def update(self, dt, tiles):
        self.get_input()
        self.vel.y += Settings.gravity * dt
        
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