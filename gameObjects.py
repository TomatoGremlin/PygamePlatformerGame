import pygame
from globalVars import TILE_SIZE,SCREEN_WIDTH


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/coin.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE // 1.5, TILE_SIZE // 1.5))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

    
heart_scale = 30       
class Heart(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image_full = pygame.transform.scale( pygame.image.load('assets/heart_full.png'), (heart_scale + 5, heart_scale  ) )  
		self.image_half =  pygame.transform.scale(pygame.image.load('assets/heart_half.png'), (heart_scale + 5, heart_scale))
		self.image_empty = pygame.transform.scale( pygame.image.load('assets/heart_empty.png'), (heart_scale + 5, heart_scale) )

		self.image = self.image_full  # Start with full heart image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, LIVES):
		if LIVES == 3:
			self.image = self.image_full
		elif  LIVES == 2:
			self.image = self.image_half
		else:
			self.image = self.image_empty
   
	def draw(self, screen):
		screen.blit(self.image, self.rect)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/exit.png')
		if(x > SCREEN_WIDTH/2 ):
			img = pygame.transform.flip(img, True, False)
		self.image = pygame.transform.scale(img, (TILE_SIZE, int(TILE_SIZE * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	