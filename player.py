ACC = 1  # acceleration rate
VEL_FLAP = -9  # flap instant velocity
VEL_MAX = 10  # max velocity

class Player():
    '''holds images, updates position and performs player action'''
    def __init__(self, images, animation_pattern, x, y):
        self.images = images  # images used for animation
        self.animation_pattern = animation_pattern  # animation pattern
        self.image = images[next(animation_pattern)]  # get first image
        self.rect = self.image.get_rect()  # rectangle from image
        # initial position
        self.rect.x = x
        self.rect.y = y
        self.velocity = VEL_FLAP

    def update(self):
        '''update player position'''
        if self.velocity < VEL_MAX:
            self.velocity += ACC  # increase velocity for each update
        self.rect.y += self.velocity  # change position based on velocity

    def animate(self):
        '''change current image to the next in cycle'''
        self.image = self.images[next(self.animation_pattern)]

    def flap(self):
        '''change player instant velocity'''
        self.velocity = VEL_FLAP
