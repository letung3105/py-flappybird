import pygame
import pygame.locals
import random
import sys
from helpers import load_images, show_score, game_over
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

# all images' data used for the game
IMAGES = {}


def get_random_pipes(pipe_pos_x=SCREENWIDTH+10):
    ''' generate a pair of pipes with random y-position '''
    # y-position of the gap
    gap_pos_y = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    # shift the gap to be closer to ground
    gap_pos_y += int(BASEY * 0.2)
    pipe_height = IMAGES['upipe'].get_height()
    return (
        Pipe(IMAGES['upipe'], pipe_pos_x, gap_pos_y - pipe_height),
        Pipe(IMAGES['lpipe'], pipe_pos_x, gap_pos_y + PIPEGAPSIZE)
    )


def main():
    global IMAGES
    # initialize pygame
    pygame.init()
    # set game's screen size
    screen = pygame.display.set_mode(SCREENSIZE)
    # delay time to get constant fps
    clock = pygame.time.Clock()

    # current frame in 1 sec
    frames = 1

    # load all images
    IMAGES = load_images()

    # initial pipes
    first_pipes = get_random_pipes()
    second_pipes = get_random_pipes(SCREENWIDTH + 10 + int(SCREENWIDTH / 2))

    # groups contain all upper and lower pipes
    upper_pipes = pygame.sprite.Group(first_pipes[0], second_pipes[0])
    lower_pipes = pygame.sprite.Group(first_pipes[1], second_pipes[1])

    # create new player
    player = Player(IMAGES['player'])
    # set player's initial position
    player.rect.x = int(SCREENWIDTH / 4 - player.rect.w / 2)
    player.rect.y = int((SCREENHEIGHT - player.rect.h) / 2)

    # player's score
    score = 0

    while True:
        # check for spacebar and up arrow presses
        for evt in pygame.event.get():
            if (evt.type == pygame.locals.KEYDOWN and
                    (evt.key == pygame.locals.K_SPACE or
                        evt.key == pygame.locals.K_UP)):
                if player.rect.y > -1 * player.rect.h:
                    player.flap()

        # check if player crashed into the ground
        if player.rect.bottom >= BASEY - 1:
            game_over(screen, IMAGES, player, BASEY, upper_pipes, lower_pipes, score)

        # loop through every pipes
        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            # check if player crashed into the pipes
            ## pixel bitmask collision, only for CustomSprite
            # if player.pixel_collide(upipe) or player.pixel_collide(lpipe):
            #     game_over(screen, IMAGES, player, BASEY, upper_pipes, lower_pipes, score)
            ## rect collision
            if pygame.sprite.collide_rect(player, upipe) or pygame.sprite.collide_rect(player, lpipe):
                game_over(screen, IMAGES, player, BASEY, upper_pipes, lower_pipes, score)
            # remove pipes if it moves off-screen
            if upipe.rect.x < -upipe.rect.w:
                upipe.kill()
            if lpipe.rect.x < -lpipe.rect.w:
                lpipe.kill()
            if 0 < upipe.rect.x < 4:
                pipes = get_random_pipes()
                upper_pipes.add(pipes[0])
                lower_pipes.add(pipes[1])
            # update score if player passed a pipe
            if upipe.rect.centerx <= player.rect.centerx < upipe.rect.centerx + 3:
                score += 1

        # update player sprite
        player.update(frames)

        # update all pipes sprite
        upper_pipes.update()
        lower_pipes.update()

        # put images on screen
        screen.blit(IMAGES['background'], (0, 0))
        screen.blit(player.image, player.rect)
        upper_pipes.draw(screen)
        lower_pipes.draw(screen)
        screen.blit(IMAGES['base'], (0, BASEY))

        # put digits on screen based on score
        show_score(screen, IMAGES['digits'], score)

        # updated frame counts and reset at 30
        frames += 1
        if frames % 30 == 0:
            frames = 1
        # refresh screen at given FPS
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
