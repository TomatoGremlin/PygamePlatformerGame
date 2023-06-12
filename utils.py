import pygame
from os import path
from globalVars import screen
import pickle


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def load_data(level):
    if path.exists(f'levels/level{level}_data'):
        pickle_in = open(f'levels/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        return world_data


