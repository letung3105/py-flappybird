from helpers import CustomSprite
import pygame


ACC = 1  # acceleration rate
VEL_FLAP = -9  # flap instant velocity
VEL_MAX = 10  # max velocity
VEL_ROT = -3  # angular velocity
ROT_MAX = -90


class Player(CustomSprite):
    '''holds images, updates position and performs player action'''
    def __init__(self, images, animation_pattern, x, y):
        self.images = images  # images used for animation
        self.animation_pattern = animation_pattern  # animation pattern
        self.image_index = next(animation_pattern)
        self.image = images[self.image_index]  # get first image
        self.rect = self.image.get_rect()  # rectangle from image
        # initial position
        self.rect.x = x
        self.rect.y = y
        self.velocity = VEL_FLAP
        self.rot = 20

    def update(self):
        '''update player position'''
        if self.velocity < VEL_MAX:
            self.velocity += ACC  # increase velocity for each update
        if self.rot > ROT_MAX:
            self.rot += VEL_ROT
        self.image = pygame.transform.rotate(
            self.images[self.image_index], self.rot
        )
        x, y = self.rect.left, self.rect.top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.y += self.velocity  # change position based on velocity

    def animate(self):
        '''change current image to the next in cycle'''
        self.image_index = next(self.animation_pattern)
        self.image = pygame.transform.rotate(
            self.images[self.image_index], self.rot
        )
        x, y = self.rect.left, self.rect.top
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def flap(self):
        '''change player instant velocity'''
        self.velocity = VEL_FLAP
        self.rot = 20
