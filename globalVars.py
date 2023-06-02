import pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#define FONT_BIG
FONT_BIG = pygame.font.SysFont('Lucida Sans', 70)
FONT_SMALL = pygame.font.SysFont('Lucida Sans', 30)


#define game variables
TILE_SIZE = 50
game_over = 0
main_menu = True

level = 2
MAX_LEVELS = 2
score = 0


#define colours
WHITE = (255, 255, 255)
BLUE_DARK = (26, 32, 44)
BLUE_LIGHT = (142, 166, 254)


