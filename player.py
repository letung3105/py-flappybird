import pygame
from itertools import cycle

PLAYER_MAX_Y_VEL = 10
PLAYER_Y_ACC = 1
PLAYER_Y_VEL_FLAP = -9


class Player(pygame.sprite.Sprite):
    """ stores player information """
    def __init__(self, images):
        super().__init__()
        return

    """ update player position and animation """
    def update(self, current_frame):
        return

    def flap(self):
        return
