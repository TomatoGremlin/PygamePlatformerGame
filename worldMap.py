import pygame
from globalVars import*
from gameObjects  import*
from obstacles import*
from utils import load_data
from loadFiles import dirt_img, grass_img, cave_img, lava2_img

obstacle_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

class World():
	def __init__(self, data):
		self.tile_list = []

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = dirt_img
					img_rect = img.get_rect()
					img_rect.x, img_rect.y  = col_count * TILE_SIZE, row_count * TILE_SIZE
					collision_rect = img_rect

					tile = (img, img_rect, collision_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = grass_img
					img_rect = img.get_rect()
					img_rect.x, img_rect.y  = col_count * TILE_SIZE, row_count * TILE_SIZE
     
					OFFSET_Y = 10  
					collision_rect = pygame.Rect(img_rect.left, img_rect.top + OFFSET_Y, img_rect.width, img_rect.height - OFFSET_Y)
					tile = (img, img_rect, collision_rect)
					self.tile_list.append(tile)
					
				if tile == 3:
					obstacle = Obstacle(col_count * TILE_SIZE, row_count * TILE_SIZE + 15)
					obstacle_group.add(obstacle)
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
				if tile == 9:
					img = cave_img
					img_rect = img.get_rect()
					img_rect.x, img_rect.y  = col_count * TILE_SIZE, row_count * TILE_SIZE
					collision_rect = img_rect

					tile = (img, img_rect, collision_rect)
					self.tile_list.append(tile)
				if tile == 10:
					img = lava2_img
					img_rect = img.get_rect()
					img_rect.x, img_rect.y  = col_count * TILE_SIZE, row_count * TILE_SIZE
					collision_rect = img_rect

					tile = (img, img_rect, collision_rect)
					self.tile_list.append(tile)
			
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

	def getrectangles(self):
		collision_rects = []
		for tile in self.tile_list:
			collision_rects.append(tile[2])  # Append the collision rectangle to the list
		return collision_rects
     


#load in level data and create world
world = World(load_data(level))