import pygame
from Player import Player
from Monster import Monster


class Game:
    def __init__(self, selected_level):
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

    def spawn_monster(self):
        self.monsters_in_screen += 1
        monster = Monster(self)
        self.all_monster.add(monster)
        self.nb_monsters -=1

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def get_score(self):
        return 'score :' + str(self.score)