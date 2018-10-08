import pygame
import pygame.locals
import random
import sys
from helpers import load_images, show_score, game_over
from player import Player
from pipe import Pipe

# set fps and screen's size
FPS = 30
# in pixels
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# y-position of ground
BASEY = SCREENHEIGHT * 0.8
# gap's size of the upper pipe and lower pipe
PIPEGAPSIZE = 100

# all images' data used for the game
IMAGES = {}


def get_random_pipes(pipe_pos_x=SCREENWIDTH+10):
    """ generate a pair of pipes with random y-position """
    return


def main():
    global IMAGES
    return


if __name__ == '__main__':
    main()
