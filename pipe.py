from helpers import SpriteWithHitmask

# number of pixel each pipe moves per frame
PIPE_X_VEL = -4


class Pipe(SpriteWithHitmask):
    """ Pipe class contains sprite with its bitmask """
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.hitmask = self.get_hitmask(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

    """ Move pipe by -4 pixels """
    def update(self):
        self.rect.x += PIPE_X_VEL
