import pygame
from globalVars import TILE_SIZE
from loadFiles import lava_img, obstacle_image

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
     
		pygame.sprite.Sprite.__init__(self)
		self.image = obstacle_image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
     
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1
   
   
   
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
     
		pygame.sprite.Sprite.__init__(self)
		self.image = lava_img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y