import pygame
import pygame.locals
import random
import sys
from helpers import getHitmask, pixelCollision
from itertools import cycle

# set fps and screen size
FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)

# y-position of the ground
BASEY = SCREENHEIGHT * 0.8
# size of gap  between the upper and lower pipe
PIPEGAPSIZE = 100

# physics connstants
PLAYERYVELMAX = 10  # player max downward velocity
PLAYERYVELMIN = -8  # player max upward velocity
PLAYERYVELFLAP = -9  # player velocity when hit spacebar
PLAYERYACC = 1  # player acceleration rate for every frame

PIPEXVEL = -4  # pipe velocity


# Keep track of all images
IMAGES = {}
HITMASKS = {}


def get_random_pipe():
    gap_pos_y = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gap_pos_y += int(BASEY * 0.2)
    pipe_height = IMAGES['lpipe'].get_height()
    pipe_pos_x = SCREENWIDTH + 10
    return [
        {'x': pipe_pos_x, 'y': gap_pos_y - pipe_height},
        {'x': pipe_pos_x, 'y': gap_pos_y + PIPEGAPSIZE}
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


def check_crash(player_info, upper_pipes, lower_pipes):
    player_info['h'] = IMAGES['player'][player_info['index']].get_height()
    player_info['w'] = IMAGES['player'][player_info['index']].get_width()
    if player_info['y'] + player_info['h'] >= BASEY - 1:
        return True
    else:
        player_rect = pygame.Rect(
            player_info['x'], player_info['y'],
            player_info['w'], player_info['h'],
        )

        player_hitmask = HITMASKS['player'][player_info['index']]
        upipe_hitmask = HITMASKS['upipe']
        lpipe_hitmask = HITMASKS['lpipe']

        pipe_w = IMAGES['upipe'].get_width()
        pipe_h = IMAGES['upipe'].get_height()
        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            upipe_rect = pygame.Rect(upipe['x'], upipe['y'], pipe_w, pipe_h)
            lpipe_rect = pygame.Rect(lpipe['x'], lpipe['y'], pipe_w, pipe_h)
            ucollide = pixelCollision(player_rect, upipe_rect, player_hitmask, upipe_hitmask)
            lcollide = pixelCollision(player_rect, lpipe_rect, player_hitmask, lpipe_hitmask)
            if ucollide or lcollide:
                return True
    return False


def game_over(screen, score):
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

    # images used
    IMAGES['background'] = pygame.image.load('./sprites/background-day.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('./sprites/base.png').convert_alpha()
    IMAGES['upipe'] = pygame.transform.rotate(
        pygame.image.load('./sprites/pipe-green.png').convert_alpha(), 180
    )
    IMAGES['lpipe'] = pygame.image.load('./sprites/pipe-green.png').convert_alpha()
    IMAGES['player'] = (
        pygame.image.load('./sprites/bluebird-upflap.png').convert_alpha(),
        pygame.image.load('./sprites/bluebird-midflap.png').convert_alpha(),
        pygame.image.load('./sprites/bluebird-downflap.png').convert_alpha(),
    )
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

    # hitmaks for pipes
    HITMASKS['upipe'] = getHitmask(IMAGES['upipe'])
    HITMASKS['lpipe'] = getHitmask(IMAGES['lpipe'])
    print(HITMASKS['lpipe'])
    print(len(HITMASKS['lpipe']))

    # hitmask for player↩
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )

    first_pipes = get_random_pipe()
    second_pipes = get_random_pipe()
    upper_pipes = [
        {'x': SCREENWIDTH + 10, 'y': first_pipes[0]['y']},
        {'x': SCREENWIDTH + 10 + int(SCREENWIDTH / 2), 'y': second_pipes[0]['y']}
    ]
    lower_pipes = [
        {'x': SCREENWIDTH + 10, 'y': first_pipes[1]['y']},
        {'x': SCREENWIDTH + 10 + int(SCREENWIDTH / 2), 'y': second_pipes[1]['y']}
    ]

    # set player's initial position
    player_pos_x = int(SCREENWIDTH / 3) - IMAGES['player'][0].get_width()
    player_pos_y = int(SCREENHEIGHT / 2) - IMAGES['player'][0].get_height()
    # create a animation loop cycle
    player_animation_cycle = cycle([0, 1, 2, 1])
    # current image used for the player
    player_frame_index = next(player_animation_cycle)
    # player's y-axis velocity
    player_y_vel = -9

    score = 0

    while True:
        for evt in pygame.event.get():
            if (evt.type == pygame.locals.KEYDOWN and
                    (evt.key == pygame.locals.K_SPACE or
                        evt.key == pygame.locals.K_UP)):
                if player_pos_y > -1 * IMAGES['player'][player_frame_index].get_height():
                    player_y_vel = PLAYERYVELFLAP

        crashed = check_crash(
            {'index': player_frame_index, 'x': player_pos_x, 'y': player_pos_y},
            upper_pipes, lower_pipes,
        )
        if crashed:
            game_over(screen, score)

        # check for score
        player_pos_x_mid = player_pos_x + IMAGES['player'][player_frame_index].get_width() / 2
        for pipe in upper_pipes:
            pipe_pos_x_mid = pipe['x'] + IMAGES['upipe'].get_width() / 2
            if pipe_pos_x_mid <= player_pos_x_mid < pipe_pos_x_mid + 4:
                score += 1

        # change player's image every 3 frames
        if frames % 3 == 0:
            player_frame_index = next(player_animation_cycle)
        # reset frames count
        if frames % 30 == 0:
            frames = 1
        # increase player y-velocity every frame
        if player_y_vel < PLAYERYVELMAX:
            player_y_vel += PLAYERYACC
        # change player position based on velocity
        player_pos_y += player_y_vel

        # change pipes position based on velocity
        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            upipe['x'] += PIPEXVEL
            lpipe['x'] += PIPEXVEL
        # add new pipe when the first reach the edge of the screen
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])
        # remove pipe when it's out of screen
        if upper_pipes[0]['x'] < -IMAGES['upipe'].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # put images on screen
        screen.blit(IMAGES['background'], (0, 0))
        screen.blit(IMAGES['base'], (0, BASEY))
        screen.blit(IMAGES['player'][player_frame_index], (player_pos_x, player_pos_y))
        for upipe, lpipe in zip(upper_pipes, lower_pipes):
            screen.blit(IMAGES['upipe'], (upipe['x'], upipe['y']))
            screen.blit(IMAGES['lpipe'], (lpipe['x'], lpipe['y']))

        show_score(screen, score)

        frames += 1
        if frames % 30 == 0:
            frames = 1
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
