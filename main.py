import pygame
from itertools import cycle
from pygame.locals import *

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# y-position of the ground
BASEY = SCREENHEIGHT * 0.8
# size of gap  between the upper and lower pipe
PIPEGAPSIZE = 100


# Fish is a inherit class of Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # list of images used to animate the flappy bird
        self._images = (
            pygame.image.load('./sprites/bluebird-upflap.png'),
            pygame.image.load('./sprites/bluebird-midflap.png'),
            pygame.image.load('./sprites/bluebird-downflap.png'),
        )
        # order of animation
        self._animation_cycle = cycle([0, 1, 2, 1])
        # current image for player
        self.img = self._images[0]
        self.rect = self.img.get_rect()

        # set player initial position
        self.rect.left = SCREENWIDTH / 3 - self.rect.size[0]
        self.rect.top = SCREENHEIGHT / 2 - self.rect.size[1]

    # loop through list of sprites for animation based on the current frame
    def animate(self, current_frame):
        self.img = self._images[next(self._animation_cycle)]


def main():
    # initialize pygame
    pygame.init()
    # set game's screen size
    screen = pygame.display.set_mode(SCREENSIZE)
    # pygame's clock used to set FPS
    clock = pygame.time.Clock()

    # current frame in 1 sec
    frames = 1

    # images used
    background = pygame.image.load('./sprites/background-day.png')
    base = pygame.image.load('./sprites/base.png')

    # Player object
    player = Player()

    while True:
        player.animate(frames)
        screen.blit(background, (0, 0))
        screen.blit(base, (0, BASEY))
        screen.blit(player.img, player.rect)

        frames += 1
        if frames % 30 == 0:
            frames = 1
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
