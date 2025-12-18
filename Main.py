# --- MAIN.PY ---

#Import Library
import os
import pygame
from settings import *
from tilemap import Tilemap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

level_path = os.path.join(BASE_DIR, "levels", "level1.txt")
dirt_path = os.path.join(BASE_DIR, "Assets", "dirt.png")

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_TITLE)
level = Tilemap(level_path, dirt_path, 16)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    level.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
