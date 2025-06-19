import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 
SIZE = {'paddle': (40,100), 'ball': (30,30)}
POS = {'player1': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 'player2': (50, WINDOW_HEIGHT / 2)}
SPEED = {'player': 500, 'ball': 450}
COLOURS = {
    'paddle': '#ee322c',
    'paddle shadow': '#b12521',
    'ball': '#ee622c',
    'ball shadow': '#c14f24',
    'bg': '#002633',
    'bg detail': '#004a63'
}