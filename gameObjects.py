import pygame
from globalVars import TILE_SIZE


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/coin.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE // 1.5, TILE_SIZE // 1.5))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/exit.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE, int(TILE_SIZE * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y