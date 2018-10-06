import pygame
from itertools import cycle

PLAYER_MAX_Y_VEL = 10
PLAYER_Y_ACC = 1
PLAYER_Y_VEL_FLAP = -9


class Player(pygame.sprite.Sprite):
    """ player class support animations and player's actions """
    def __init__(self, images):
        super().__init__()
        # images for animation
        self.images = images
        # cycle([0,1,2,1]) = 0 -> 1 -> 2 -> 1 -> 0 -> 1 -> 2 -> 1 -> 0 -> ...
        self.animation_pattern = cycle([0, 1, 2, 1])

        self.image = self.images[next(self.animation_pattern)]
        self.rect = self.image.get_rect()
        self.y_vel = -9

    """ update sprites position and animation """
    def update(self, current_frame):
        # change sprite's image every 3 frame to animate wing flaps
        if current_frame % 3 == 0:
            self.image = self.images[next(self.animation_pattern)]

        # increase player's downward velocity every frame
        if self.y_vel < PLAYER_MAX_Y_VEL:
            self.y_vel += PLAYER_Y_ACC

        # update player's y-position
        self.rect.y += self.y_vel

    def flap(self):
        self.y_vel = -9
