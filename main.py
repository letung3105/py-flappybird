import pygame
import pygame.locals
import random
import sys
from helpers import load_images
from player import Player
from pipe import Pipe

# set fps and screen's size
FPS = 30
# in pixels
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# y-position of ground
BASEY = SCREENHEIGHT * 0.8
# gap's size of the upper pipe and lower pipe
PIPEGAPSIZE = 100

IMAGES = {}  # contains all images' data used for the game


def get_random_pipes(pipe_pos_x=SCREENWIDTH+10):
    """ generate a pair of pipes with random y-position """
    return


def main():
    global IMAGES
    return

def show_score(screen, score):
    """ turns numeric score into sprites on screen """
    digits = [int(x) for x in str(score)]
    total_width = 0

    # loop through all digits
    # to calculate the total length of the number
    for digit in digits:
        total_width += IMAGES['digits'][digit].get_width()

    # offset to center the number
    x_offset = (SCREENWIDTH - total_width) / 2
    for digit in digits:
        screen.blit(IMAGES['digits'][digit], [x_offset, SCREENHEIGHT * 0.1])
        x_offset += IMAGES['digits'][digit].get_width()


def game_over(screen, player, upper_pipes, lower_pipes, score):
    """ show game over scene """
    clock = pygame.time.Clock()
    message = pygame.image.load('./sprites/gameover.png')
    message_pos_x = (SCREENWIDTH - message.get_width()) / 2
    message_pos_y = (SCREENHEIGHT - message.get_height()) / 3
    while True:
        # Press esc to quit
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
        screen.blit(IMAGES['background'], (0, 0))
        screen.blit(player.image, player.rect)
        upper_pipes.draw(screen)
        lower_pipes.draw(screen)
        screen.blit(IMAGES['base'], (0, BASEY))
        screen.blit(message, (message_pos_x, message_pos_y))
        show_score(screen, score)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
