import pygame
import pygame.locals
import random
import sys
from player import Player
from pipe import Pipe

# set fps and screen size
FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# y-position of the ground
BASEY = SCREENHEIGHT * 0.8
# size of gap  between the upper and lower pipe
PIPEGAPSIZE = 100

# Keep track of all images
IMAGES = {}
HITMASKS = {}


def get_random_pipes(pipe_pos_x=SCREENWIDTH + 10):
    gap_pos_y = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gap_pos_y += int(BASEY * 0.2)
    pipe_height = IMAGES['upipe'].get_height()
    return [
        Pipe(IMAGES['upipe'], pipe_pos_x, gap_pos_y - pipe_height),
        Pipe(IMAGES['lpipe'], pipe_pos_x, gap_pos_y + PIPEGAPSIZE)
    ]


def show_score(screen, score):
    digits = [int(x) for x in str(score)]
    total_width = 0

    for digit in digits:
        total_width += IMAGES['digits'][digit].get_width()

    x_offset = (SCREENWIDTH - total_width) / 2
    for digit in digits:
        screen.blit(IMAGES['digits'][digit], [x_offset, SCREENHEIGHT * 0.1])
        x_offset += IMAGES['digits'][digit].get_width()


def game_over(screen, player, upper_pipes, lower_pipes, score):
    clock = pygame.time.Clock()
    message = pygame.image.load('./sprites/gameover.png')
    message_pos_x = (SCREENWIDTH - message.get_width()) / 2
    message_pos_y = (SCREENHEIGHT - message.get_height()) / 2
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.locals.QUIT or
                    (event.type == pygame.locals.KEYDOWN and
                        event.key == pygame.locals.K_ESCAPE)):
                pygame.quit()
                sys.exit()
        screen.blit(IMAGES['background'], (0, 0))
        screen.blit(IMAGES['base'], (0, BASEY))
        screen.blit(player.image, player.rect)
        upper_pipes.draw(screen)
        lower_pipes.draw(screen)
        screen.blit(message, (message_pos_x, message_pos_y))
        show_score(screen, score)
        pygame.display.update()
        clock.tick(FPS)


def main():
    # initialize pygame
    pygame.init()
    # set game's screen size
    screen = pygame.display.set_mode(SCREENSIZE)
    # pygame's clock used to set FPS
    clock = pygame.time.Clock()

    # current frame in 1 sec
    frames = 1

    # background and base image
    IMAGES['background'] = pygame.image.load('./sprites/background-day.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('./sprites/base.png').convert_alpha()
    # upper and lower pipes images
    IMAGES['upipe'] = pygame.transform.rotate(
        pygame.image.load('./sprites/pipe-green.png').convert_alpha(), 180
    )
    IMAGES['lpipe'] = pygame.image.load('./sprites/pipe-green.png').convert_alpha()
    # score's digits images
    IMAGES['digits'] = (
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

    # initial pipes
    first_pipes = get_random_pipes()
    second_pipes = get_random_pipes(SCREENWIDTH + 10 + int(SCREENWIDTH / 2))
    # groups contain all upper and lower pipes
    upper_pipes = pygame.sprite.Group(first_pipes[0], second_pipes[0])
    lower_pipes = pygame.sprite.Group(first_pipes[1], second_pipes[1])

    # create new player
    player = Player()
    # set player's initial position
    player.rect.x = int(SCREENWIDTH / 3) - player.image.get_width() / 2
    player.rect.y = int(SCREENHEIGHT / 2) - player.image.get_height() / 2

    # player's score
    score = 0

    while True:
        # check for key presses
        # specifically spacebar and up arrow
        for evt in pygame.event.get():
            if (evt.type == pygame.locals.KEYDOWN and
                    (evt.key == pygame.locals.K_SPACE or
                        evt.key == pygame.locals.K_UP)):
                if player.rect.y > -1 * player.image.get_height():
                    player.flap()

        # update player position
        # and animate wing flap
        player.update(frames)

        # update all pipes position in group
        upper_pipes.update()
        lower_pipes.update()

        # check if player crashed into the ground
        if player.rect.y >= BASEY - player.image.get_height():
            game_over(screen, player, upper_pipes, lower_pipes, score)

        player_pos_x_mid = player.rect.x + player.image.get_width() / 2
        # loop through every pipes
        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            # check if player crashed into the pipes
            if player.pixel_collide(upipe) or player.pixel_collide(lpipe):
                game_over(screen, player, upper_pipes, lower_pipes, score)
            # if pygame.sprite.collide_rect(player, upipe) or pygame.sprite.collide_rect(player, lpipe):
            #     game_over(screen, player, upper_pipes, lower_pipes, score)
            # remove pipes if it moves off-screen
            if upipe.rect.x < -upipe.image.get_width():
                upipe.kill()
            if lpipe.rect.x < -lpipe.image.get_width():
                lpipe.kill()
            if 0 < upipe.rect.x < 3:
                pipes = get_random_pipes()
                upper_pipes.add(pipes[0])
                lower_pipes.add(pipes[1])
            # update score if player passed a pipe
            pipe_pos_x_mid = upipe.rect.x + upipe.image.get_width() / 2
            if pipe_pos_x_mid <= player_pos_x_mid < pipe_pos_x_mid + 3:
                score += 1

        # put images on screen
        screen.blit(IMAGES['background'], (0, 0))
        screen.blit(IMAGES['base'], (0, BASEY))
        screen.blit(player.image, player.rect)
        upper_pipes.draw(screen)
        lower_pipes.draw(screen)

        # put digits on screen based on score
        show_score(screen, score)

        # refresh screen at given FPS
        frames += 1
        if frames % 30 == 0:
            frames = 1
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
