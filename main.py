import pygame
import sys
import random
from itertools import cycle
from player import Player
from pipe import Pipe

# screen size
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
# frame-per-second
FPS = 30

Y_BASE = int(SCREEN_HEIGHT * 0.8)  # ground position from bottom of the screen
GAP_SIZE = 100  # gap between upper pipe and lower pipe


def get_pipes(x_pos=SCREEN_WIDTH+10):
    '''return a pipes pair with random gap position'''
    pipe_height = IMAGES['lpipe'].get_height()
    # random position of the gap
    gap_y_pos = random.randrange(
        int(Y_BASE * 0.2), int(Y_BASE * 0.8 - GAP_SIZE)
    )
    return {
        'u': Pipe(IMAGES['upipe'], x_pos, gap_y_pos - pipe_height),  # upper pipe
        'l': Pipe(IMAGES['lpipe'], x_pos, gap_y_pos + GAP_SIZE)  # lower pipe
    }


pygame.init()  # init pygame
# a display to put images on
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()  # used to get fixed FPS
game_over = False  # check if player crashes

# load all images used
IMAGES = {
    'player': (
        pygame.image.load("./sprites/bluebird-upflap.png"),
        pygame.image.load("./sprites/bluebird-midflap.png"),
        pygame.image.load("./sprites/bluebird-downflap.png"),
    ),

    'background': pygame.image.load("./sprites/background-day.png"),
    'base': pygame.image.load("./sprites/base.png"),
    'game_over': pygame.image.load("./sprites/gameover.png"),
    'lpipe': pygame.image.load("./sprites/pipe-green.png"),
    'upipe': pygame.transform.rotate(pygame.image.load("./sprites/pipe-green.png"), 180)
}

animation_pattern = cycle([0,1,2,1])  # 0 -> 1 -> 2 -> 1 -> ...
player = Player(
    IMAGES['player'],
    animation_pattern,
    SCREEN_WIDTH / 3 - IMAGES['player'][0].get_width() / 2,  # placed in 1/3 the width of the screen
    (SCREEN_HEIGHT - IMAGES['player'][0].get_height()) / 2  # placed in 1/2 the height of the screen
)

# first pipes
pipes = get_pipes()
# keep track of all pipes
upper_pipes = [pipes['u']]
lower_pipes = [pipes['l']]

# counting frames for animation
frames = 0

# game loop
while True:
    # get evt
    for evt in pygame.event.get():
        # quit game
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key presses
        if evt.type == pygame.KEYDOWN:
            # press esc to quit if losed
            if game_over:
                if evt.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # move player when press spacebar
            else:
                if evt.key == pygame.K_SPACE:
                    player.flap()

    if not game_over:
        player.update()  # update player position
        # animate wing flaps
        frames += 1
        if frames == 4:
            player.animate()
            frames = 0
        # crash into the ground
        if player.rect.bottom >= Y_BASE:
            game_over = True

        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            # update pipes position
            upipe.update()
            lpipe.update()
            # add new pipes when there is a pipe passes the middle of the screen
            if int(SCREEN_WIDTH) / 2 - 4 < upipe.rect.x <= int(SCREEN_WIDTH / 2):
                pipes = get_pipes()
                upper_pipes.append(pipes['u'])
                lower_pipes.append(pipes['l'])
            # crash into pipes
            if player.rect.colliderect(upipe.rect):
                game_over = True
                break
            if player.rect.colliderect(lpipe.rect):
                game_over = True
                break
        # remove pipes objects when out of screen
        # memory optimization
        if upper_pipes[0].rect.x < -IMAGES['upipe'].get_width():
            del upper_pipes[0]
        if lower_pipes[0].rect.x < -IMAGES['upipe'].get_width():
            del lower_pipes[0]

    # display images on screen
    display.blit(IMAGES['background'], (0, 0))
    display.blit(player.image, player.rect)
    for upipe, lpipe in zip(upper_pipes, lower_pipes):
        display.blit(upipe.image, upipe.rect)
        display.blit(lpipe.image, lpipe.rect)
    display.blit(IMAGES['base'], (0, Y_BASE))

    if game_over:
        display.blit(IMAGES['game_over'], (
            (SCREEN_WIDTH - IMAGES['game_over'].get_width()) / 2,
            (SCREEN_HEIGHT - IMAGES['game_over'].get_height()) / 2,
        ))

    # update game frame
    pygame.display.update()
    clock.tick(FPS)  # delay time for constant fps
