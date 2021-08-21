import clock
import pygame
from Player import Player
from Monster import Monster
from pygame.time import Clock


class Game:
    def __init__(self, selected_level, size):
        # check if game running or main menu
        self.is_playing = False
        self.size = size


        # create a sprite group to have the draw methods for group sprites
        self.all_player = pygame.sprite.Group()
        self.score = 0

        # add player to game object to be able to access it from everywhere
        self.player = Player(self)

        # add player to sprite group
        self.all_player.add(self.player)

        # create sprite group for monsters
        self.all_monster = pygame.sprite.Group()

        # list to handle keyboard and mouse events
        self.pressed = {}

        # levels [level, max nb of monsters appearing in the screen, nb monsters for this level]
        self.levels = [[1, 3, 10],
                       [2, 3, 80],
                       [3, 3, 100],
                       [4, 3, 150]]
        self.selected_level = self.levels[selected_level]
        self.nb_monsters = self.selected_level[2]
        self.max_monster = self.selected_level[1]
        self.monsters_in_screen = 0

    def game_over(self):
        # restarting the game --> making everything come back to original state
        # empty the sprite group by overwriting it with empty sprite group
        self.all_monster = pygame.sprite.Group()
        # player health back to origin
        self.player.health = self.player.maxhealth
        # game finished, back to main menu
        self.is_playing = False

    def start(self):
        # restarting the game after playing one game
        # spawning monsters
        self.nb_monsters = self.selected_level[2]
        self.max_monster = self.selected_level[1]
        self.monsters_in_screen = 0
        if self.monsters_in_screen < self.max_monster:
            if self.nb_monsters > 0:
                self.spawn_monster()

    def update(self, screen, myfont, clock):
        # check if there is less than 3 monsters appearing in the screen
        if self.monsters_in_screen < self.max_monster:
            if self.nb_monsters > 0:
                # if there is still monsters left to appear make it appear
                self.spawn_monster()
        # update the position of the player image
        screen.blit(self.player.image, self.player.rect)
        # get the cursor position to print the cursor img
        m_pos = pygame.mouse.get_pos()
        # update the cursor img position at each frame
        screen.blit(self.player.cursor_img,
                    (m_pos[0] - self.player.cursor_img.get_width() / 2,
                     m_pos[1] - self.player.cursor_img.get_height() / 2))

        # draw the labels with color and position and text
        label_score = myfont.render('Score : ' + str(self.score), (0, 0, 0), (255, 255, 0))
        label_enemy = myfont.render('Enemys remaining :' + str(self.nb_monsters), (0, 0, 0), (255, 255, 0))
        label_level = myfont.render('Level ' + str(self.selected_level[0]), (0, 0, 0), (255, 255, 255, 0))
        label_fps = myfont.render('FPS : ' + str(int(clock.get_fps())), (0, 0, 0), (255, 255, 255, 0))
        screen.blit(label_level, (450, 10))
        screen.blit(label_enemy, (780, 10))
        screen.blit(label_score, (150, 10))
        screen.blit(label_fps, (10, 10))

        # rotation of the cursor
        self.player.rotate_cursor()

        # draw all monsters on screen (img & position)
        self.all_monster.draw(screen)
        self.player.update_health_bar(screen)

        # check if player is jumping
        self.player.jump()

        # update position of each projectile (model)
        for p in self.player.all_projectiles:
            p.move()

        # update position of all monsters (moving forward) and img
        for m in self.all_monster:
            m.forward()
            m.update_health_bar(screen)

        # update position of all projectile
        self.player.all_projectiles.draw(screen)

        # jump methods make the player img not coming back to original position but 5 px over or under so it is
        # correcting the problem
        if not self.player.isJumping and self.player.rect.y < self.player.y_origin:
            self.player.rect.y += 5
        if not self.player.isJumping and self.player.rect.y > self.player.y_origin:
            self.player.rect.y -= 5

        # keychecking if right or left using a list of the key used in the game. Security to handle only 1 strike
        # event if keeping pressed

        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        if self.pressed.get(pygame.K_q) and self.player.rect.x > 0:
            self.player.move_left()
        if not self.player.isJumping:
            if self.pressed.get(pygame.K_SPACE):
                self.player.isJumping = True

    # make monster spawn one by one and add it to the sprite group and modify value of monsters in screen and nb
    # monsters remaining
    def spawn_monster(self):
        self.monsters_in_screen += 1
        monster = Monster(self)
        self.all_monster.add(monster)
        self.nb_monsters -= 1

    # check if monster is in collision with player
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    # return the score
    def get_score(self):
        return 'score :' + str(self.score)
