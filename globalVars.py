import pygame

WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#font
font = pygame.font.SysFont('Lucida Sans', 70)
font_score = pygame.font.SysFont('Lucida Sans', 30)

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
