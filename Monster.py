import random

import pygame


class Monster(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.maxhealth = 100
        self.attack = 0.3
        self.image = pygame.image.load('assets/mummy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(800, 1000, step=100)
        self.rect.y = 540
        self.velocity = random.randrange(1, 5)

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 12, self.rect.y - 20, self.maxhealth, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 12, self.rect.y - 20, self.health, 5])

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.kill()
            self.game.score += 1
            self.game.monsters_in_screen -=1



    def forward(self):

        if not self.game.check_collision(self, self.game.all_player):
            if self.game.player.rect.x < self.rect.x:
                    self.rect.x -= self.velocity
            else:
                    self.rect.x += self.velocity
        else:
            self.game.player.damage(self.attack)