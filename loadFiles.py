import pygame
from pygame import mixer
from globalVars import TILE_SIZE, SCREEN_WIDTH , SCREEN_HEIGHT
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#IMAGES
bg_img = pygame.transform.scale(pygame.image.load('assets/sky.png') , (SCREEN_WIDTH, SCREEN_HEIGHT))

start_img = pygame.transform.scale(pygame.image.load('assets/start_btn.png') , (120, 50))
exit_img = pygame.transform.scale(pygame.image.load('assets/exit_btn.png') , (150, 50)) 
restart_img = pygame.transform.scale(pygame.image.load('assets/restart_btn.png') , (150, 50))
go_img = pygame.transform.scale(pygame.image.load('assets/go_btn.png') , (70, 30))


#SOUNDS
pygame.mixer.music.load('assets/music/background/my-little-garden-of-eden-112845.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('assets/music/reward.mp3')
coin_fx.set_volume(0.3)
jump_fx = pygame.mixer.Sound('assets/music/jump.mp3')
jump_fx.set_volume(0.2)
game_over_fx = pygame.mixer.Sound('assets/music/beefmow.mp3')
game_over_fx.set_volume(0.3)
victory_fx =  pygame.mixer.Sound('assets/music/winsquare-6993.mp3')
victory_fx.set_volume(0.3)
click_fx = pygame.mixer.Sound('assets/music/mixkit-quick-win-video-game-notification-269.wav')
click_fx.set_volume(0.15)
