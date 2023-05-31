import pygame

#IMAGES
sun_img = pygame.image.load('assets/sun.png')
bg_img = pygame.image.load('assets/sky.png')
restart_img = pygame.image.load('assets/restart.png')
start_img = pygame.image.load('assets/start.png')
exit_img = pygame.image.load('assets/exit_btn.png')

#SOUNDS
pygame.mixer.music.load('assets/music/cottagecore.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
fish_collected_fx = pygame.mixer.Sound('assets/music/reward.mp3')
fish_collected_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('assets/music/jump.mp3')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('assets/music/beefmow.mp3')
game_over_fx.set_volume(0.5)