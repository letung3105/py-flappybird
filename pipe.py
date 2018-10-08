import pygame

# number of pixel each pipe moves per frame
PIPE_X_VEL = -4


class Pipe(pygame.sprite.Sprite):
    ''' pipe's sprite control '''
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        # image of pipe
        self.image = image
        # rectangle section of image
        self.rect = self.image.get_rect()
        # set initial position
        self.rect.x = pos_x
        self.rect.y = pos_y

    ''' update pipe position '''
    def update(self):
        self.rect.x += PIPE_X_VEL
