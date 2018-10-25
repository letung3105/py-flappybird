import pygame
import random

# display size
DISPLAY_HEIGHT = 512
DISPLAY_WIDTH = 288
# ground position
BASE_Y = DISPLAY_HEIGHT * 0.8
# distant between upper and lower pipe
GAP_SIZE = 100
# number of frames per sec
FPS = 30

def get_pipes(x=DISPLAY_WIDTH+10):
    '''create randomly generated pipes pair'''
    pipe_height = IMAGES['lower_pipe'].get_height()
    # random gap position
    gap_y = random.randrange(int(BASE_Y*0.2), int(BASE_Y*0.8-GAP_SIZE))
    # create upper pipe rect from image and set its position
    upper_rect = IMAGES['upper_pipe'].get_rect()
    upper_rect.x = x
    upper_rect.y = gap_y - pipe_height
    # create lower pipe rect from image and set its position
    lower_rect = IMAGES['lower_pipe'].get_rect()
    lower_rect.x = x
    lower_rect.y = gap_y + GAP_SIZE
    return (upper_rect, lower_rect)

# start pygame
pygame.init()

# setup game display screen
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# clock for fixing FPS
clock = pygame.time.Clock()

# all images
IMAGES = {
    "background": pygame.image.load("./sprites/background-night.png"),
    "bird": pygame.image.load("./sprites/bluebird-midflap.png"),
    "lower_pipe": pygame.image.load("./sprites/pipe-green.png"),
    "upper_pipe": pygame.transform.rotate(
        pygame.image.load("./sprites/pipe-red.png"),
        180
    ),
    "base": pygame.image.load("./sprites/base.png"),
    "game_over": pygame.image.load("./sprites/gameover.png"),
}

# pixels per frame
velocity = -9
flap_velocity = -9
pipe_velocity = -5

# pixels per frame^2
acc = 1

# check if the player crashed
game_over = False

# bird initial position
player_rect = IMAGES['bird'].get_rect()
player_rect.x = (DISPLAY_WIDTH / 3) - IMAGES['bird'].get_width() / 2
player_rect.y = (DISPLAY_HEIGHT / 2) - IMAGES['bird'].get_height() / 2

# initial pipes pair
upipe, lpipe = get_pipes()

# lists contain all pipes
upper_pipes = [upipe]
lower_pipes = [lpipe]

# main game loop
while True:
    # check for event, i.e., player input
    for event in pygame.event.get():
        # check window close event
        if event.type == pygame.QUIT:
            pygame.quit()
        # check key presss
        if event.type == pygame.KEYDOWN:
            # change velocity when spacebar is pressed
            if event.key == pygame.K_SPACE and player_rect.y >= -IMAGES['bird'].get_height() and not game_over:
                velocity = flap_velocity
    # end game if bird touches ground
    if player_rect.y >= BASE_Y - IMAGES['bird'].get_height():
        game_over = True
    # update images position when bird has not crashed
    if not game_over:
        # increased velocity every frame
        velocity += acc
        # change bird position based on velocity
        player_rect.y += velocity
        # move pipes to the left
        for lpipe, upipe in zip(lower_pipes, upper_pipes):
            lpipe.x += pipe_velocity
            upipe.x += pipe_velocity
            # check if bird touches the pipe
            if player_rect.colliderect(lpipe) or player_rect.colliderect(upipe):
                game_over = True
                break
        # add new pipe when one of the pipe passes the middle of the screen
        for lpipe, upipe in zip(lower_pipes, upper_pipes):
            if (DISPLAY_WIDTH/2) < lpipe.x <= (DISPLAY_WIDTH/2) - pipe_velocity:
                new_upipe, new_lpipe = get_pipes()
                upper_pipes.append(new_upipe)
                lower_pipes.append(new_lpipe)
                break
        # delete pipes from list when out of screen
        for index, lpipe in enumerate(lower_pipes):
            if lpipe.x < -IMAGES['lower_pipe'].get_width():
                lower_pipes.pop(index)
                upper_pipes.pop(index)
                break

    # add images to screen
    display.blit(IMAGES['background'], (0, 0))
    display.blit(IMAGES['bird'], player_rect)
    for upipe, lpipe in zip(upper_pipes, lower_pipes):
        display.blit(IMAGES['upper_pipe'], upipe)
        display.blit(IMAGES['lower_pipe'], lpipe)
    display.blit(IMAGES['base'], (0, BASE_Y))
    # display game over message if crashed
    if game_over:
        msg_x = (DISPLAY_WIDTH - IMAGES['game_over'].get_width()) / 2 
        msg_y = (DISPLAY_HEIGHT - IMAGES['game_over'].get_height()) / 2 
        display.blit(IMAGES['game_over'], (msg_x, msg_y))
    # refresh screen
    pygame.display.update()
    # delay time to achieve to correct FPS
    clock.tick(FPS)
