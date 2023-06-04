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
from player import*
from Pygame_Lights import*

pygame.display.set_caption(GAME_NAME)




	
		


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

		#--- LEVEL CHOOSING -----#
		'''draw_text("↑ ↓ Starting Level: " + str(level), FONT_SMALL, WHITE, (SCREEN_WIDTH // 2) - 90, SCREEN_HEIGHT // 2 + 110)
		for event in pygame.event.get():
			if event.type == pygame.K_UP:
				level -= 1
				if level < 1:
					level = MAX_LEVELS
			elif event.type == pygame.KEYDOWN:
				level += 1
				if level > MAX_LEVELS:
					level = 1 '''
     
		#----------------------------------
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
			'''world_data = []
			world = reset_level(level)'''
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

		game_over,lives,  fade_counter = player.update(game_over, lives,  fade_counter, world)
		
  
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