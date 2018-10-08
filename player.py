import pygame
from itertools import cycle

PLAYER_MAX_Y_VEL = 10  # max downward velocity
PLAYER_Y_ACC = 1  # acceleration constant
PLAYER_Y_VEL_FLAP = -9  # flap instant velocity


class Player(pygame.sprite.Sprite):
    ''' player animations and actions '''
    def __init__(self, images):
        super().__init__()

    ''' update sprites position and animation '''
    def update(self, current_frame):

    ''' change instant velocity when flap '''
    def flap(self):
        return
