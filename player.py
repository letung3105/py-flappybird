import pygame
from itertools import cycle

PLAYER_MAX_Y_VEL = 10  # max downward velocity
PLAYER_Y_ACC = 1  # acceleration constant
PLAYER_Y_VEL_FLAP = -9  # flap instant velocity


class Player(pygame.sprite.Sprite):
    ''' player animations and actions '''
    def __init__(self, images):
        super().__init__()
        # images for animation
        self.images = images
        # cycle([0,1,2,1]) = 0 -> 1 -> 2 -> 1 -> 0 -> 1 -> 2 -> 1 -> 0 -> ...
        self.animation_pattern = cycle([0, 1, 2, 1])
        # image of player
        self.image = self.images[next(self.animation_pattern)]
        # rectangle section of image
        self.rect = self.image.get_rect()
        # initial instant velocity
        self.y_vel = -9

    ''' update sprites position and animation '''
    def update(self, current_frame):
        # change sprite's image every 3 frame to animate wing flaps
        if current_frame % 3 == 0:
            self.image = self.images[next(self.animation_pattern)]

        # increase player velocity every frame
        if self.y_vel < PLAYER_MAX_Y_VEL:
            self.y_vel += PLAYER_Y_ACC

        # update player y-position
        self.rect.y += self.y_vel

    ''' change instant velocity when flap '''
    def flap(self):
        self.y_vel = PLAYER_Y_VEL_FLAP
