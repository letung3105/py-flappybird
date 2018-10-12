import pygame
import sys
import random
from itertools import cycle
from player import Player
from pipe import Pipe

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
Y_BASE = int(SCREEN_HEIGHT * 0.8)
GAP_SIZE = 100

def get_pipes(x_pos=SCREEN_WIDTH+10):
    pipe_height = IMAGES['lpipe'].get_height()
    gap_y_pos = random.randrange(
        int(Y_BASE * 0.2), int(Y_BASE * 0.8 - GAP_SIZE)
    )
    return {
        'u': Pipe(IMAGES['upipe'], x_pos, gap_y_pos - pipe_height),
        'l': Pipe(IMAGES['lpipe'], x_pos, gap_y_pos + GAP_SIZE)
    }


pygame.init()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_over = False

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

animation_pattern = cycle([0,1,2,1])
player = Player(
    IMAGES['player'],
    animation_pattern,
    SCREEN_WIDTH / 3 - IMAGES['player'][0].get_width() / 2,
    (SCREEN_HEIGHT - IMAGES['player'][0].get_height()) / 2
)

pipes = get_pipes()
upper_pipes = [pipes['u']]
lower_pipes = [pipes['l']]

frames = 0

while True:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evt.type == pygame.KEYDOWN:
            if game_over:
                if evt.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                if evt.key == pygame.K_SPACE:
                    player.flap()

    if not game_over:
        player.update()
        frames += 1
        if frames == 4:
            player.animate()
            frames = 0
        if player.rect.bottom >= Y_BASE:
            game_over = True

        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            upipe.update()
            lpipe.update()
            if int(SCREEN_WIDTH) / 2 - 4 < upipe.rect.x <= int(SCREEN_WIDTH / 2):
                pipes = get_pipes()
                upper_pipes.append(pipes['u'])
                lower_pipes.append(pipes['l'])
            if player.rect.colliderect(upipe.rect):
                game_over = True
                break
            if player.rect.colliderect(lpipe.rect):
                game_over = True
                break
        if upper_pipes[0].rect.x < -IMAGES['upipe'].get_width():
            del upper_pipes[0]
        if lower_pipes[0].rect.x < -IMAGES['upipe'].get_width():
            del lower_pipes[0]

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

    pygame.display.update()
    clock.tick(30)
