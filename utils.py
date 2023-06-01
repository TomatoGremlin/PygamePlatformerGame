import pygame
from globalVars import screen
import pickle


def draw_text(text, FONT_BIG, text_col, x, y):
	img = FONT_BIG.render(text, True, text_col)
	screen.blit(img, (x, y))

def load_data(level):
    pickle_in = open(f'levels/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    return world_data