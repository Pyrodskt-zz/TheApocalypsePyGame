import pygame
from Player import Player
from Monster import Monster


class Game:
    def __init__(self):
        self.all_player = pygame.sprite.Group()
        self.score = 0
        self.player = Player(self)
        self.all_player.add(self.player)
        self.all_monster = pygame.sprite.Group()
        self.pressed = {}
        self.level = [1, 10]
        self.max_monster = 3
        self.monsters_in_screen = 0
        self.nb_monsters = self.level[1]
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster()

    def spawn_monster(self):
        self.monsters_in_screen += 1
        monster = Monster(self)
        self.all_monster.add(monster)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def get_score(self):
        return 'score :' + str(self.score)