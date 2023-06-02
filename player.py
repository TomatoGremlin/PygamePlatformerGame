import pygame
from loadFiles import jump_fx, game_over_fx
from globalVars import*
from utils import*
from worldMap import blob_group, exit_group, lava_group, platform_group, world

class Player():
	def __init__(self, x, y):
		self.reset(x, y)


	def update(self, game_over, fade_counter):
		dx, dy = 0, 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
    
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.in_air:
			
				if self.direction == 1:
					self.image = self.images_jumping_right[self.counter // walk_cooldown % len(self.images_jumping_right)]
				elif self.direction == -1:
					self.image = self.images_jumping_left[self.counter // walk_cooldown % len(self.images_jumping_right)]
				self.counter = 0  # Reset the counter to prevent frame switching during jump

			else:
				if self.counter > walk_cooldown:
					self.counter = 0	
					self.index += 1
					if self.index >= len(self.images_right):
						self.index = 0
					if self.direction == 1:
						self.image = self.images_right[self.index]
					if self.direction == -1:
						self.image = self.images_left[self.index]
  

			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[2].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[2].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[2].bottom - self.rect.top 
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[2].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			if fade_counter < SCREEN_WIDTH:
				fade_counter += 5 
				for y in range(0, 6, 2):
					pygame.draw.rect(screen, WHITE, (0, y * 100, fade_counter, SCREEN_HEIGHT  ))
					pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - fade_counter, y*100, SCREEN_WIDTH, SCREEN_HEIGHT ))
   
			draw_text('GAME OVER!', FONT_BIG, BLUE_DARK, (SCREEN_WIDTH // 2) - 200, SCREEN_HEIGHT // 2)
			if self.rect.y > -SCREEN_HEIGHT:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over, fade_counter


	def reset(self, x, y):

		self.images_right, self.images_left  = [], []
		self.images_jumping_right, self.images_jumping_left  = [], []
		self.index, self.counter = 0, 0
  
		for num in range(1, 5):
			img_right = pygame.image.load(f'assets/cat{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 40))
			img_left = pygame.transform.flip(img_right, True, False)
   
			img_jumping_right = pygame.image.load(f'assets/cat_jump1.png')
			img_jumping_right = pygame.transform.scale(img_jumping_right, (40, 40))
			img_jumping_left = pygame.transform.flip(img_jumping_right, True, False)

			self.images_right.append(img_right)
			self.images_left.append(img_left)
			self.images_jumping_right.append(img_jumping_right)
			self.images_jumping_left.append(img_jumping_left)

   
		self.dead_image = pygame.transform.scale( pygame.image.load('assets/ghost.png'), (40,40) )
              
		self.image = self.images_right[self.index]

		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.width, self.height  = self.image.get_width(), self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True
