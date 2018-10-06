import pygame
import random


# all paths to images
PATHS = {}

PATHS['backgrounds'] = (
    './sprites/background-day.png',
    './sprites/background-night.png'
)

PATHS['base'] = './sprites/base.png'

PATHS['pipes'] = (
    "./sprites/pipe-red.png",
    "./sprites/pipe-green.png"
)

PATHS['digits'] = (
    './sprites/0.png',
    './sprites/1.png',
    './sprites/2.png',
    './sprites/3.png',
    './sprites/4.png',
    './sprites/5.png',
    './sprites/6.png',
    './sprites/7.png',
    './sprites/8.png',
    './sprites/9.png',
)

PATHS['player'] = (
    (
        './sprites/bluebird-upflap.png',
        './sprites/bluebird-midflap.png',
        './sprites/bluebird-downflap.png',
    ),
    (
        './sprites/yellowbird-upflap.png',
        './sprites/yellowbird-midflap.png',
        './sprites/yellowbird-downflap.png',
    ),
    (
        './sprites/redbird-upflap.png',
        './sprites/redbird-midflap.png',
        './sprites/redbird-downflap.png',
    )
)


def load_images():
    images = {}
    # background and base image
    rand_background = random.choice(PATHS['backgrounds'])
    images['background'] = pygame.image.load(rand_background).convert_alpha()
    images['base'] = pygame.image.load('./sprites/base.png').convert_alpha()

    # upper and lower pipes images
    rand_pipe = random.choice(PATHS['pipes'])
    images['upipe'] = pygame.transform.rotate(
        pygame.image.load(rand_pipe).convert_alpha(), 180
    )
    images['lpipe'] = pygame.image.load(rand_pipe).convert_alpha()

    rand_player = random.choice(PATHS['player'])
    images['player'] = (
        pygame.image.load(rand_player[0]).convert_alpha(),
        pygame.image.load(rand_player[1]).convert_alpha(),
        pygame.image.load(rand_player[2]).convert_alpha(),
    )

    # score's digits images
    images['digits'] = (
        pygame.image.load('./sprites/0.png').convert_alpha(),
        pygame.image.load('./sprites/1.png').convert_alpha(),
        pygame.image.load('./sprites/2.png').convert_alpha(),
        pygame.image.load('./sprites/3.png').convert_alpha(),
        pygame.image.load('./sprites/4.png').convert_alpha(),
        pygame.image.load('./sprites/5.png').convert_alpha(),
        pygame.image.load('./sprites/6.png').convert_alpha(),
        pygame.image.load('./sprites/7.png').convert_alpha(),
        pygame.image.load('./sprites/8.png').convert_alpha(),
        pygame.image.load('./sprites/9.png').convert_alpha(),
    )
    return images


class CustomSprite(pygame.sprite.Sprite):
    """pygame.Sprite with pixel bitmask collision detection"""
    def __init__(self):
        super().__init__()

    """ get bit mask from image """
    def get_bitmask(self):
        mask = []
        for x in range(self.image.get_width()):
            mask.append([])
            for y in range(self.image.get_height()):
                mask[x].append(bool(self.image.get_at((x, y))[3]))
        return mask

    """ check for collision with other based on  bitmask"""
    def pixel_collide(self, other):
        # rectangle cross section of this sprite with other
        rect = self.rect.clip(other.rect)
        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - self.rect.x, rect.y - self.rect.y
        x2, y2 = rect.x - other.rect.x, rect.y - other.rect.y

        # check every pixel in the cross section for collision
        # i.e both bit are True
        bitmask1 = self.get_bitmask()
        bitmask2 = other.get_bitmask()
        for x in range(rect.width):
            for y in range(rect.height):
                if bitmask1[x1 + x][y1 + y] and bitmask2[x2 + x][y2 + y]:
                    return True
        return False