import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

from globalVars import *
from assetsLoading import *
from damageInducers import *
from fish import Fish
from platforms import Platform
from button import Button

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
FPS = 60


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def reset_level(level):
	player.reset(100, HEIGHT - 130)
	blob_group.empty()
	platform_group.empty()
	fish_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
 
	#dummy fish next to the  score
	score_fish = Fish(TILE_SIZE // 2, TILE_SIZE // 2)
	fish_group.add(score_fish)
	return world


#======================================== PLAYER =====================================================
class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, isGameOver):
		x_speed = 0
		y_speed = 0
		walk_cooldown = 5
		col_thresh = 20

		if isGameOver == 0:
			#### KEY MOVEMENT INPUTS ####
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				x_speed -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				x_speed += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#### ANIMATION HANDLING ####
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			####------GRAVITY----- ####
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			y_speed += self.vel_y

			#COLLISION
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + x_speed, self.rect.y, self.width, self.height):
					x_speed = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + y_speed, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						y_speed = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						y_speed = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#ENEMY COLLISION
			if pygame.sprite.spritecollide(self, blob_group, False):
				isGameOver = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				isGameOver = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				isGameOver = 1


			# PLATFORM COLLISION
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + x_speed, self.rect.y, self.width, self.height):
					x_speed = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + y_speed, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + y_speed) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						y_speed = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + y_speed) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						y_speed = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += x_speed
			self.rect.y += y_speed


		elif isGameOver == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, BLUE, (WIDTH // 2) - 200, HEIGHT // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return isGameOver


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'assets/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('assets/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True




#========================================== WORLD =====================================================
class World():
	def __init__(self, data):
		dirt_img = pygame.image.load('assets/dirt.png')
		grass_img = pygame.image.load('assets/grass.png')

		self.tile_list = []
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZE
					img_rect.y = row_count * TILE_SIZE
					tile = (img, img_rect)
					self.tile_list.append(tile)
     
				if tile == 2:
					img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
					img_rect = img.get_rect()
					img_rect.x = col_count * TILE_SIZE
					img_rect.y = row_count * TILE_SIZE
					tile = (img, img_rect)
					self.tile_list.append(tile)
     
				if tile == 3:
					blob = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE + 15)
					blob_group.add(blob)
     
				if tile == 4:
					platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 1, 0)
					platform_group.add(platform)
     
				if tile == 5:
					platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, 0, 1)
					platform_group.add(platform)
     
				if tile == 6:
					lava = Lava(col_count * TILE_SIZE, row_count * TILE_SIZE + (TILE_SIZE // 2))
					lava_group.add(lava)
     
				if tile == 7:
					fish = Fish(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE + (TILE_SIZE // 2))
					fish_group.add(fish)
     
				if tile == 8:
					exit = Exit(col_count * TILE_SIZE, row_count * TILE_SIZE - (TILE_SIZE // 2))
					exit_group.add(exit)
     
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


#========================================== EXIT =====================================================
class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('assets/exit.png')
		self.image = pygame.transform.scale(img, (TILE_SIZE, int( TILE_SIZE * 1.5 )))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



#========================================== CREATING INSTANCES OF THE CLASSES =====================================================
player = Player(100, HEIGHT - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
    
#load in level data and create world
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)




#========================================== GAME LOOP =====================================================
def main():
    #create dummy fish for showing the score
    score_fish = Fish(TILE_SIZE // 2, TILE_SIZE // 2)
    fish_group.add(score_fish) 
    
    restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 100, restart_img)
    start_button = Button(WIDTH // 2 - 350, HEIGHT // 2, start_img)
    exit_button = Button(WIDTH // 2 + 150, HEIGHT // 2, exit_img)
    
    
    run = True
    while run:

        clock.tick(FPS)

        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))

        if mainMenu == True:
            if exit_button.draw():
                run = False
            if start_button.draw():
                mainMenu = False
        else:
            world.draw()

            if isGameOver == 0:
                blob_group.update()
                platform_group.update()
                #update score
                #check if a fish has been collected
                if pygame.sprite.spritecollide(player, fish_group, True):
                    score += 1
                    fish_collected_fx.play()
                draw_text('X ' + str(score), font_score, WHITE, TILE_SIZE - 10, 10)
            
            blob_group.draw(screen)
            platform_group.draw(screen)
            lava_group.draw(screen)
            fish_group.draw(screen)
            exit_group.draw(screen)

            isGameOver = player.update(isGameOver)

            #if player has died
            if isGameOver == -1:
                if restart_button.draw():
                    world_data = []
                    world = reset_level(level)
                    isGameOver = 0
                    score = 0

            #if player has completed the level
            if isGameOver == 1:
                #reset game and go to next level
                level += 1
                if level <= max_levels:
                    #reset level
                    world_data = []
                    world = reset_level(level)
                    isGameOver = 0
                else:
                    draw_text('GAME WON', font, BLUE, (WIDTH // 2) - 140, HEIGHT // 2)
                    if restart_button.draw():
                        level = 1
                        #reset level
                        world_data = []
                        world = reset_level(level)
                        isGameOver = 0
                        score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    
    
    
    
main()