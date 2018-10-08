import pygame

# number of pixel each pipe moves per frame
PIPE_X_VEL = -4


class Pipe(pygame.sprite.Sprite):
    ''' pipe data '''
    def __init__(self, image, pos_x, pos_y):
        super().__init__()

    ''' update pipe position '''
    def update(self):
        return
