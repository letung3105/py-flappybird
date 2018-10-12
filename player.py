import pygame


ACCLERATION = 1
FLAP_VELOCITY = -9
MAX_VELOCITY = 10

class Player():
    def __init__(self, images, animation_pattern, x, y):
        self.images = images
        self.animation_pattern = animation_pattern
        self.image = images[next(animation_pattern)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0

    def update(self):
        if self.velocity < MAX_VELOCITY:
            self.velocity += ACCLERATION
        self.rect.y += self.velocity

    def animate(self):
        self.image = self.images[next(self.animation_pattern)]

    def flap(self):
        self.velocity = FLAP_VELOCITY
