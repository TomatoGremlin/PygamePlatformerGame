import pygame
from loadFiles import jump_fx, game_over_fx
from globalVars import*
from utils import*
from worldMap import *
from loadFiles import ghost_img

class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def animate_player(self, walking_cooldown):
		if self.in_air or self.jumped:
			if self.direction == 1:
				self.image = self.images_jumping_right[self.counter // walking_cooldown % len(self.images_jumping_right)]
			elif self.direction == -1:
				self.image = self.images_jumping_left[self.counter // walking_cooldown % len(self.images_jumping_right)]
		else:
			if not self.ducked:
				if self.counter > walking_cooldown:
					self.counter = 0
					self.index = (self.index + 1) % len(self.images_right)
					if self.direction == 1:
						self.image = self.images_right[self.index]
					elif self.direction == -1:
						self.image = self.images_left[self.index]

 	
	def add_gravity(self, speed_y ):
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		speed_y += self.vel_y

		return speed_y


	def check_collision(self, game_over, LIVES):
		#OBSTACLE COLLISION
		if pygame.sprite.spritecollide(self, blob_group, False) or pygame.sprite.spritecollide(self, lava_group, False) :
			game_over_fx.play()
			if LIVES != 1:
				LIVES-= 1
				player.reset(100, SCREEN_HEIGHT - 70 )
			else:
				game_over = -1

		#EXIT COLLISION
		if pygame.sprite.spritecollide(self, exit_group, False):
			game_over = 1

		return game_over, LIVES


	def update(self, game_over, LIVES , fade_counter, world):
		speed_x, speed_y = 0, 0
		walking_cooldown = 5
		col_thresh = 20

		if game_over == 0:
      
			# -----KEYPRESSES-----#
			key = pygame.key.get_pressed()
			# JUMP
			if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True

			if not key[pygame.K_SPACE]:
				self.jumped = False

			# GO RIGHT
			if key[pygame.K_RIGHT]:
				speed_x += 5
				self.counter += 1
				self.direction = 1

			# GO LEFT
			if key[pygame.K_LEFT]:
				speed_x -= 5
				self.counter += 1
				self.direction = -1

			# DUCK DOWN
			if key[pygame.K_d]:
				self.ducked = True
				if self.direction == 1:
					self.image = self.duck_image_right
				elif self.direction == -1:
					self.image = self.duck_image_left
			else:
				self.ducked = False

				if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
					self.counter = 0
					self.index = 0

					if self.direction == 1:
						self.image = self.images_right[self.index]
					elif self.direction == -1:
						self.image = self.images_left[self.index]



			#----ANIMATION----#
			self.animate_player(walking_cooldown)
  

			#---ADDING GRAVITY---#
			speed_y = self.add_gravity(speed_y)

			#-------COLLISION CHECKS: ------#
			#TILES
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[2].colliderect(self.rect.x + speed_x, self.rect.y, self.width, self.height):
					speed_x = 0
				#check for collision in y direction
				if tile[2].colliderect(self.rect.x, self.rect.y + speed_y, self.width, self.height):
					#check if player hits the top of a block
					if self.vel_y < 0:
						speed_y = tile[2].bottom - self.rect.top 
						self.vel_y = 0
					#check if player hits bottom of a block
					elif self.vel_y >= 0:
						speed_y = tile[2].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#ENEMY COLLISION & LAVA COLLISION or EXIT
			game_over, LIVES = self.check_collision(game_over, LIVES)


			#PLATFORMS COLLISION
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + speed_x, self.rect.y, self.width, self.height):
					speed_x = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + speed_y, self.width, self.height):
					#check if player is below a platform
					if abs((self.rect.top + speed_y) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						speed_y = platform.rect.bottom - self.rect.top
					#check if player is above a platform
					elif abs((self.rect.bottom + speed_y) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						speed_y = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#UPDATE PLAYER COORDINATES
			self.rect.x += speed_x
			self.rect.y += speed_y
		
  
		# When Player Dies - Closing Screen
		elif game_over == -1:
			self.image = self.dead_image
			if fade_counter < SCREEN_WIDTH:
				fade_counter += 5 
				for y in range(0, 6, 2):
					pygame.draw.rect(screen, WHITE, (0, y * 100, fade_counter, SCREEN_HEIGHT  ))
					pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - fade_counter, y*100, SCREEN_WIDTH, SCREEN_HEIGHT ))
   
			draw_text('GAME OVER!', FONT_BIG, PINK, (SCREEN_WIDTH // 2) - 200, SCREEN_HEIGHT // 2)
			if self.rect.y > -SCREEN_HEIGHT:
				self.rect.y -= 5

    

		#draw player onto screen
		screen.blit(self.image, self.rect)
		return game_over, LIVES, fade_counter


	def reset(self, x, y):
		self.images_right, self.images_left  = [], []
		self.images_jumping_right, self.images_jumping_left  = [], []
		self.index, self.counter = 0, 0
  
		for num in range(1, 5):
			img_right = pygame.image.load(f'assets/cat{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 40))
			img_left = pygame.transform.flip(img_right, True, False)
   
			img_jumping_right = pygame.image.load(f'assets/cat_jump{num}.png')
			img_jumping_right = pygame.transform.scale(img_jumping_right, (40, 40))
			img_jumping_left = pygame.transform.flip(img_jumping_right, True, False)
			
			self.duck_image_right =  pygame.image.load(f'assets/cat3.png')
			self.duck_image_right = pygame.transform.scale(self.duck_image_right, (40, 40))
			self.duck_image_left =  pygame.transform.flip(self.duck_image_right, True, False)

			self.images_right.append(img_right)
			self.images_left.append(img_left)
			self.images_jumping_right.append(img_jumping_right)
			self.images_jumping_left.append(img_jumping_left)

		self.dead_image = ghost_img     
		self.image = self.images_right[self.index]

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.width, self.height  = self.image.get_width(), self.image.get_height()
		self.vel_y = 0

		self.jumped = False
		self.direction = 0
		self.in_air = True 
		self.ducked = False


player = Player(100, SCREEN_HEIGHT - 130)
		