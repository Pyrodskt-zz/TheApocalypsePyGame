import math

import pygame


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, angle):
        # init parent class to define it is a sprite object
        super().__init__()

        # inherit player to use its functions and parameters
        self.player = player

        # load projectile img and resize
        self.image = pygame.image.load('assets/projectile.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.player.game.size.calc_x(50), self.player.game.size.calc_y(50)))
        self.origin_image = self.image

        # define projectile velocity
        self.velocity = 10

        # create rectangle to handle interactions
        self.rect = self.image.get_rect()

        # place it to the right arm of the player that's why +120 & +80
        self.rect.x = player.rect.x + self.player.game.size.calc_x(120)
        self.rect.y = player.rect.y + self.player.game.size.calc_y(80)

        # save the starting point of the projectile
        self.f_x = self.rect.x
        self.f_y = self.rect.y

        self.angle_proj = angle

        # calculation of the next position knowing the angler calculated in the player class
        self.change_x = math.cos(self.angle_proj) * self.velocity
        self.change_y = math.sin(self.angle_proj) * self.velocity

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        # move the projectile knowing the origin and destination
        self.f_x += self.change_x
        self.f_y += self.change_y
        self.rect.x = self.f_x
        self.rect.y = self.f_y

        # if collision with a monster apply damages and remove the projectile
        for monster in self.player.game.check_collision(self, self.player.game.all_monster):
            self.remove()
            monster.damage(self.player.attack)

        # if getting out of the screen remove the projectile
        if self.rect.x > self.player.game.size.screen[0] or self.rect.y > self.player.game.size.screen[1]:
            self.remove()
