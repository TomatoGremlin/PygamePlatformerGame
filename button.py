import pygame
from globalVars import screen
from loadFiles import click_fx


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				click_fx.play()
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)
		return action
  
	def update(self, image):
		self.image = image
	
	def toggle(self, is_music_playing, music_on, music_off):
		if is_music_playing:
			self.update(music_on)  # Set button image to "play" state
		else:
			self.update(music_off)  # Set button image to "pause" state