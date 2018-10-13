from helpers import CustomSprite
VEL_PIPE = -4

class Pipe(CustomSprite):
    '''update position'''
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image  # image used for pipe (upper / lower)
        self.rect = self.image.get_rect()  # rectangle from image
        # initial position
        self.rect.x = x
        self.rect.y = y

    def update(self):
        '''change pipe position'''
        self.rect.x += VEL_PIPE
