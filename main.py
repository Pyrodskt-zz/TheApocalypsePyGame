import math
from win32api import GetSystemMetrics
import pygame

from pygame.time import Clock
from Size import Size
from Game import Game

# init of the game obj
pygame.init()
# init of the timer to set the fps limit
clock = pygame.time.Clock()
pygame.display.set_caption('The Apocalypse')
pygame.event.set_allowed([pygame.QUIT,pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
# set the screen size and background
screen = pygame.display.set_mode((GetSystemMetrics(0)-1, GetSystemMetrics(1)-60))

#create object to convert the size of the imgs depending on the size of the screen
size = Size(screen.get_width(), screen.get_height())

background = pygame.image.load('assets/bg.jpg').convert_alpha()
# banner of the main menu
banner = pygame.image.load('assets/banner.png').convert_alpha()
# resize of the image of the banner
banner = pygame.transform.scale(banner, (size.calc_x(500) , size.calc_y(500)))
banner_rect = banner.get_rect()
# get the middle position of the screen
banner_rect.x = math.ceil(size.screen[0] / 4)

# button of the main menu
play_button = pygame.image.load('assets/button.png').convert_alpha()
play_button = pygame.transform.scale(play_button, (size.calc_x(400), size.calc_y(150)))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil((size.screen[0] / 3.33))
play_button_rect.y = math.ceil(size.screen[1]/2) + size.calc_y(100)


# create a font with color and size
myfont = pygame.font.SysFont("monospace", 25)

# init of a new game obj which contain the player and the keyboard interactions
game = Game(2, size)
running = True

while running:
    # set FPS
    clock.tick(60)
    # update background at each frame
    screen.blit(background, (background.get_rect().x /2, -200))
    # check if game running or main menu running
    if game.is_playing:
        game.update(screen, myfont, clock)
    else:
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    pygame.display.flip()
    for event in pygame.event.get():
        # keyboard and mouse interactions
        # closing app/game
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # if mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # if game not running check if clicking play button
            if not game.is_playing:
                if play_button_rect.collidepoint(event.pos):
                    game.is_playing = True
                    game.start()
            # else checking which button is clicked
            else:
                click_state = pygame.mouse.get_pressed()
                game.pressed[event.type] = True

                # left click
                if click_state[0]:
                    game.player.lauch_projectile()

        #elif event.type == pygame.MOUSEBUTTONUP:
        #    game.pressed[event.type] = False

            # security to ignore key kept pressed and only count it one time
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False



