import pygame
from Comet import Comet

class CometFallEvent:

    def __init__(self, game):
        self.game = game

        self.percent = 100
        self.percent_speed = 3
        self.nb_comets = 0
        self.max_nb_comets = 50
        self.all_comets = pygame.sprite.Group()

    def meteor_fall(self):
        if self.nb_comets < self.max_nb_comets:

            self.all_comets.add(Comet(self.game))
            self.nb_comets +=1
    def is_full_loaded(self):
        return self.percent >= 100

    def attempt_fall(self):
        if self.is_full_loaded():
            print('pluie de cometes')
            self.meteor_fall()
            self.percent = 0

    def add_percent(self):

        self.percent += self.percent_speed

    def update_bar(self, surface):
        self.attempt_fall()
        #pygame.draw.rect(surface, (187, 11, 11),
                         #[self.game.size.calc_x(20), self.game.size.calc_y(40),
                          #((surface.get_width()-40) /100) * self.percent, 10])
