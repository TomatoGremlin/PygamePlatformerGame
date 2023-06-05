import pygame
from pygame.locals import *

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
start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 30, start_img)
exit_button = Button(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 30,  exit_img)
restart_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 100, restart_img)
go_button = Button(SCREEN_WIDTH - 140, 10,  go_img)
music_button = Button(SCREEN_WIDTH - 60, 10,  music_on_img)


def reset_level(level):
	player.reset(100, SCREEN_HEIGHT - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	world = World(load_data(level))
 
	#create dummy coin for showing the score
	score_coin = Coin(TILE_SIZE // 2, TILE_SIZE // 2)
	coin_group.add(score_coin)
	return world



# ---LIGHT-----#
light_size = 300
light_color = (255, 200, 30)  
light_intensity = 0.3
light = LIGHT( light_size, pixel_shader(light_size, light_color, light_intensity, point=True ))
#-------------------
run = True
while run:
	clock.tick(FPS)
	screen.blit(bg_img, (0, 0))

	#----- MAIN MENU SCREEN ----#
	if main_menu == True:
		draw_text(GAME_NAME, FONT_MID, BLUE_DARK, (SCREEN_WIDTH // 2) - 220, SCREEN_HEIGHT // 2 - 50)

		#--- LEVEL CHOOSING -----#
		draw_text("↑ ↓ Starting Level: " + str(level), FONT_SMALL, WHITE, (SCREEN_WIDTH // 2) - 90, SCREEN_HEIGHT // 2 + 110)
		#----------------------------------
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
			world_data = []
			world = reset_level(level)
   
	else:
     
    #----GAME----#
		world.draw()
		# Draw game objects on screen
		blob_group.draw(screen)
		platform_group.draw(screen)
  
	 	## Draw a black overlay on the background: ##
		overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 160))  # alpha value  == transparency
		screen.blit(overlay, (0, 0))

		# Update and Draw the heart for LIVES
		heart.update(LIVES)
		heart.draw(screen)
  
  		# Change Levels
		draw_text("↑ ↓ Go To Level: " + str(level), FONT_SMALL, WHITE, SCREEN_WIDTH - 320, 10 )
		if go_button.draw():
			world_data = []
			world = reset_level(level)
			score = 0
			LIVES = 3
			heart.update

		
    	#-------------------------------------------#
		if game_over == 0:
			blob_group.update()
			platform_group.update()
			#UPDATE SCORE - check if coin is collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), FONT_SMALL, BLUE_LIGHT, TILE_SIZE - 10, 10)
		
		# Draw game objects on screen
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		#Update player Coordinates
		game_over, LIVES,  fade_counter = player.update(game_over, LIVES,  fade_counter, world)
  
  		#---- Update the light position ----#
		light_x = player.rect.centerx
		light_y = player.rect.centery
		collision_rects = world.getrectangles()  # Get the collision rectangles from of the map
        # Pass the screen and collision_rects as arguments to light.main()
		light.main( collision_rects, screen, light_x, light_y, )
		
  
		#--- A) player has died --- #
		if game_over == -1:
			if restart_button.draw():
				fade_counter = 0
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
				LIVES = 3
				heart.update
	
		#-- B) player has completed the level---- #
		if game_over == 1 :

			#-----RESET GAME & GO TO THE NEXT LEVEL---#
			level += 1
			if level <= MAX_LEVELS:
				#---RESET LEVEL----#
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				rect_width = SCREEN_WIDTH
				rect_height = 80
				rectangle_x = (SCREEN_WIDTH // 2) - (rect_width // 2)
				rectangle_y = (SCREEN_HEIGHT // 2) - (rect_height // 2) + 50
				pygame.draw.rect(screen, BLUE_LIGHT, (rectangle_x, rectangle_y, rect_width, rect_height))

				draw_text('VICTORY', FONT_BIG, BLUE_DARK, (SCREEN_WIDTH // 2) - 160, SCREEN_HEIGHT // 2)
				if restart_button.draw():
					level = 1
					#---RESET LEVEL----#
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0
					LIVES = 3
					heart.update


 	#CLOSE WINDOW / CHANGE LEVEL ↑ ↓ / TOGGLE MUSIC:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False	
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				print("----------")
				level += 1
				if level > MAX_LEVELS:
					level = 1 
			elif event.key == pygame.K_DOWN:
				print("true")
				level -= 1
				if level < 1:
					level = MAX_LEVELS
		if event.type == pygame.MOUSEBUTTONDOWN:
			# Check if the music button was clicked
			if music_button.draw():
				# Toggle the music state
				is_music_playing = not is_music_playing
				
				if is_music_playing:
					# Start playing music
					pygame.mixer.music.play()
				else:
					# Stop playing music
					pygame.mixer.music.stop()
				# Update the music button image
				music_button.toggle(is_music_playing, music_on_img, music_off_img)
	music_button.draw()
	pygame.display.update()

pygame.quit()