import pygame
from globalVars import TILE_SIZE


class Fish(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/fish.png').convert_alpha()
		self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)