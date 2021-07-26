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
        self.nb_monster = 10
        self.spawn_monster()
        self.spawn_monster()

    def spawn_monster(self):
        monster = Monster(self)
        self.all_monster.add(monster)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def get_score(self):
        return 'score :' + str(self.score)