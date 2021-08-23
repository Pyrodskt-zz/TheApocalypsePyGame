import pygame
import random

class Comet(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/comet.png')
        self.image = pygame.transform.scale(self.image, (self.game.size.calc_x(70), self.game.size.calc_y(70)))
        self.rect = self.image.get_rect()

        self.velocity = 2

        self.spawn = random.randint(20, self.game.size.screen[0] - 70)
        self.rect.x = self.spawn


    def fall(self):
        self.rect.y += self.velocity

        if self.rect.y > self.game.size.screen[1]:
            self.remove()