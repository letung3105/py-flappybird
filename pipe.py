from helpers import CustomSprite

# number of pixel each pipe moves per frame
PIPE_X_VEL = -4


class Pipe(CustomSprite):
    """ pipe inherits from """
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

    """ move pipe by -4 pixels """
    def update(self):
        self.rect.x += PIPE_X_VEL
