import pygame
from globalVars import  SCREEN_WIDTH
from loadFiles import coin_img, exit_level_img, full_img, half_img, empty_img


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = coin_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

    
class Heart(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image_full = full_img
		self.image_half =  half_img
		self.image_empty =  empty_img

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
		if( x > SCREEN_WIDTH // 2 ):
			img = pygame.transform.flip(img, True, False)
		self.image = exit_level_img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	