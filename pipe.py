import pygame

# number of pixel each pipe moves per frame
PIPE_X_VEL = -4


class Pipe(pygame.sprite.Sprite):
    """ stores pipe information """
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        return

    """ update pipe sprite """
    def update(self):
        return