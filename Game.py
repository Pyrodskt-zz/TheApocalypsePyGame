import clock
import pygame
from Player import Player
from Monster import Monster
from pygame.time import Clock


class Game:
    def __init__(self, selected_level):
        self.is_playing = False
        self.all_player = pygame.sprite.Group()
        self.score = 0
        self.player = Player(self)
        self.all_player.add(self.player)
        self.all_monster = pygame.sprite.Group()
        self.pressed = {}
        self.levels = [[1, 3, 10],
                       [2, 3, 20],
                       [3, 3, 30],
                       [4, 3, 40]]
        self.selected_level = self.levels[selected_level]
        self.nb_monsters = self.selected_level[2]
        self.max_monster = self.selected_level[1]
        self.monsters_in_screen = 0

    def game_over(self):
        self.all_monster = pygame.sprite.Group()
        self.player.health = self.player.maxhealth
        self.is_playing = False


    def start(self):
        print(self.selected_level)
        self.nb_monsters = self.selected_level[2]
        self.max_monster = self.selected_level[1]
        self.monsters_in_screen = 0
        if self.monsters_in_screen < self.max_monster:
            if self.nb_monsters > 0:
                self.spawn_monster()

    def update(self, screen, myfont, clock):
        if self.monsters_in_screen < self.max_monster:
            if self.nb_monsters > 0:
                self.spawn_monster()
        screen.blit(self.player.image, self.player.rect)
        m_pos = pygame.mouse.get_pos()
        # update the target scope position at each frame
        screen.blit(self.player.cursor_img,
                    (m_pos[0] - self.player.cursor_img.get_width() / 2,
                     m_pos[1] - self.player.cursor_img.get_height() / 2))
        # rotation of the cursor
        label_score = myfont.render('Score : ' + str(self.score), (0, 0, 0), (255, 255, 0))
        label_enemy = myfont.render('Enemys remaining :' + str(self.nb_monsters), (0, 0, 0), (255, 255, 0))
        label_level = myfont.render('Level ' + str(self.selected_level[0]), (0, 0, 0), (255, 255, 255, 0))
        label_fps = myfont.render('FPS : ' + str(int(clock.get_fps())), (0, 0, 0), (255, 255, 255, 0))
        screen.blit(label_level, (450, 10))
        screen.blit(label_enemy, (780, 10))
        screen.blit(label_score, (150, 10))
        screen.blit(label_fps, (10, 10))

        self.player.rotate_cursor()
        self.all_monster.draw(screen)
        self.player.update_health_bar(screen)
        self.player.jump()

        # locking fps to 60

        # update position of each projectile (model)
        for p in self.player.all_projectiles:
            p.move()

        for m in self.all_monster:
            m.forward()
            m.update_health_bar(screen)
            # update position of each projectile (view)
        self.player.all_projectiles.draw(screen)

        if not self.player.isJumping and self.player.rect.y < self.player.y_origin:
            self.player.rect.y += 5
        if not self.player.isJumping and self.player.rect.y > self.player.y_origin:
            self.player.rect.y -= 5
            # keychecking if right or left using a list of the key used in the game. Security to handle only 1 strike event if keeping pressed
        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        if self.pressed.get(pygame.K_q) and self.player.rect.x > 0:
            self.player.move_left()
        if not self.player.isJumping:
            if self.pressed.get(pygame.K_SPACE):
                self.player.isJumping = True

    def spawn_monster(self):
        self.monsters_in_screen += 1
        monster = Monster(self)
        self.all_monster.add(monster)
        self.nb_monsters -= 1

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def get_score(self):
        return 'score :' + str(self.score)
