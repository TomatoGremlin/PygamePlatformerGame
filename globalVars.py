import pygame
import os

WIDTH = 900
HEIGHT = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))



#game variables
TILE_SIZE = 50
isGameOver = 0
mainMenu = True 
level = 3
max_levels = 7
score = 0

#colours
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
