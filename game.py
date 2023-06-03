import pygame
from pygame.locals import *
from os import path

from button import*
from gameObjects import*
from globalVars import*
from loadFiles import*
from obstacles import*
from utils import*
from worldMap import*
#from player import*
from Pygame_Lights import*

pygame.display.set_caption(GAME_NAME)

class Player():
	def __init__(self, x, y):
		self.reset(x, y)


	def update(self, game_over, lives , fade_counter):
		dx, dy = 0, 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#-----KEYPRESSES-----#
			key = pygame.key.get_pressed()
			#JUMP
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:

				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			#GO RIGHT
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			#GO LEFT
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1

			#DUCK DOWN
			if key[pygame.K_d]:
				self.ducked = True
				if self.direction == 1:
					self.image = self.duck_image_right
				elif self.direction == -1:
					self.image = self.duck_image_left
			else:

				if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
					self.counter = 0
					self.index = 0
		
					if self.direction == 1:
						self.image = self.images_right[self.index]
					if self.direction == -1:
						self.image = self.images_left[self.index]


			#----ANIMATION----#
			if self.in_air == True or self.jumped == True:
				if self.direction == 1:
					self.image = self.images_jumping_right[self.counter // walk_cooldown % len(self.images_jumping_right)]
				elif self.direction == -1:
					self.image = self.images_jumping_left[self.counter // walk_cooldown % len(self.images_jumping_right)]

			else:
				if self.counter > walk_cooldown and self.ducked == False:
					self.counter = 0	
					self.index += 1
					if self.index >= len(self.images_right):
						self.index = 0
					if self.direction == 1:
						self.image = self.images_right[self.index]
					if self.direction == -1:
						self.image = self.images_left[self.index]
  

			#---ADDING GRAVITY---#
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#-------COLLISION CHECKS: ------#
			#TILES
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[2].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[2].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if player hits the top of a block
					if self.vel_y < 0:

						dy = tile[2].bottom - self.rect.top 
						self.vel_y = 0
					#check if player hits bottom of a block
					elif self.vel_y >= 0:
						dy = tile[2].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#ENEMY COLLISION
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over_fx.play()
				if lives != 0:
					lives-= 1
					player.reset(100, SCREEN_HEIGHT - 70 )
				else:
					game_over = -1

			#LAVA COLLISION
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over_fx.play()
				if lives != 0:
					lives-= 1
					player.reset(100, SCREEN_HEIGHT - 70 )
				else:
					game_over = -1
	
			#EXIT COLLISION
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#PLATFORMS COLLISION
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


			#UPDATE PLAYER COORDINATES
			self.rect.x += dx
			self.rect.y += dy
		
			
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

		return game_over, lives ,fade_counter


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

   
		self.dead_image = pygame.transform.scale( pygame.image.load('assets/ghost.png'), (40,40) )
              
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

#DUMMY COLLECTABLE TO SHOW NEXT TO SCORE
score_coin = Coin(TILE_SIZE // 2, TILE_SIZE // 2)
coin_group.add(score_coin)

heart = Heart( TILE_SIZE // 2 + 70, TILE_SIZE // 2 - 15)

#CREATING BUTTONS
restart_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100, restart_img)
start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 30,  exit_img)

def reset_level(level):
	player.reset(100, SCREEN_HEIGHT - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'levels/level{level}_data'):
		pickle_in = open(f'levels/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
 
	#create dummy coin for showing the score
	score_coin = Coin(TILE_SIZE // 2, TILE_SIZE // 2)
	coin_group.add(score_coin)

	return world



# ---LIGHT-----#
light_size = 300
light_color = (255, 200, 30)  
light_intensity = 0.3
light = LIGHT(light_size, pixel_shader(light_size, light_color, light_intensity, point=True))
#-------------------
fade_counter = 0
run = True
while run:
	clock.tick(FPS)
	screen.blit(bg_img, (0, 0))

	#----- MAIN MENU SCREEN ----#
	if main_menu == True:
		draw_text(GAME_NAME, FONT_MID, BLUE_DARK, (SCREEN_WIDTH // 2) - 220, SCREEN_HEIGHT // 2 - 50)
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
    #----GAME----#
    
		world.draw()
	 	## Draw a black overlay on the background: ##
		overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 160))  # Adjust the alpha value as desired
		screen.blit(overlay, (0, 0))

		# Draw hearts for lives
		heart.update(lives)
		heart.draw(screen)
  
		if game_over == 0:
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), FONT_SMALL, BLUE_LIGHT, TILE_SIZE - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over,lives,  fade_counter = player.update(game_over, lives,  fade_counter)
		
  
  		#---- Update the light position ----#
		light_x = player.rect.centerx
		light_y = player.rect.centery
		collision_rects = world.getrectangles()  # Get the collision rectangles from of the map
        # Pass the screen and collision_rects as arguments to light.main()
		light.main(collision_rects, screen, light_x, light_y, )
		

  
		#--- if player has died --- #
   

		if game_over == -1:
			if restart_button.draw():
				fade_counter = 0
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
				lives = 3
				heart.update

			

		#-- if player has completed the level---- #
		if game_over == 1:
			#-----RESET GAME & GO TO THE NEXT LEVEL---#
			level += 1
			if level <= MAX_LEVELS:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				rect_width = SCREEN_WIDTH
				rect_height = 80
				rectangle_x = (SCREEN_WIDTH // 2) - (rect_width // 2)
				rectangle_y = (SCREEN_HEIGHT // 2) - (rect_height // 2) + 50
				pygame.draw.rect(screen, BLUE_LIGHT, (rectangle_x, rectangle_y, rect_width, rect_height))

				draw_text('YOU WIN!', FONT_BIG, BLUE_DARK, (SCREEN_WIDTH // 2) - 160, SCREEN_HEIGHT // 2)
				if restart_button.draw():
					level = 1
					#---RESET LEVEL----#
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0
					lives = 3
					heart.update



 	#CLOSE WINDOW:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()