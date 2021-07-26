import math

import pygame
from pygame.time import Clock

from Game import Game

# init of the game obj
pygame.init()

# init of the timer to set the fps limit
clock = pygame.time.Clock()
pygame.display.set_caption('The Apocalypse')


# set the screen size and background
screen = pygame.display.set_mode((1080, 720))
background = pygame.image.load('assets/bg.jpg')

myfont = pygame.font.SysFont("monospace", 25)

# init of a new game obj which contain the player and the keyboard interactions
game = Game()
running = True

while running:
    # update background at each frame
    screen.blit(background, (0, -200))
    # update the player position at each frame using the rectangle of the player and his position
    screen.blit(game.player.image, game.player.rect)
    m_pos = pygame.mouse.get_pos()
    # update the target scope position at each frame
    screen.blit(game.player.cursor_img,
                (m_pos[0] - game.player.cursor_img.get_width() / 2, m_pos[1] - game.player.cursor_img.get_height() / 2))
    # rotation of the cursor
    label = myfont.render('Score : ' + str(game.score), (0, 0, 0), (255, 255, 0))
    screen.blit(label, (10, 10))
    game.player.rotate_cursor()
    game.all_monster.draw(screen)
    game.player.update_health_bar(screen)
    game.player.jump()
    # locking fps to 60
    clock.tick(60)

    # update position of each projectile (model)
    for p in game.player.all_projectiles:
        p.move()

    for m in game.all_monster:
        m.forward()
        m.update_health_bar(screen)
        # update position of each projectile (view)
    game.player.all_projectiles.draw(screen)
    pygame.display.flip()

    if not game.player.isJumping and game.player.rect.y < game.player.y_origin:
        game.player.rect.y += 5
    if not game.player.isJumping and game.player.rect.y > game.player.y_origin:
        game.player.rect.y -= 5
        # keychecking if right or left using a list of the key used in the game. Security to handle only 1 strike event if keeping pressed
    if game.pressed.get(pygame.K_d) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()
    if game.pressed.get(pygame.K_q) and game.player.rect.x > 0:
        game.player.move_left()
    if not game.player.isJumping:
        if game.pressed.get(pygame.K_SPACE):
            game.player.isJumping = True

    for event in pygame.event.get():
        # keyboard and mouse interraction
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print('[main] --> Fermeture du jeu')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_state = pygame.mouse.get_pressed()
            game.pressed[event.type] = True
            if click_state[0]:
                game.player.lauch_projectile()
            if click_state[1]:
                print('scroll click')
            if click_state[2]:
                print('left click')
        elif event.type == pygame.MOUSEBUTTONUP:
            game.pressed[event.type] = False

            # another part of the security to ignore key kept pressed
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
