import math

import pygame



class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, angle):
        super().__init__()
        self.player = player

        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.origin_image = self.image

        self.velocity = 15
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.angle_img = 0
        self.f_x = self.rect.x
        self.f_y = self.rect.y

        self.angle_proj = angle
        self.change_x = math.cos(self.angle_proj) * self.velocity
        self.change_y = math.sin(self.angle_proj) * self.velocity

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        # self.rotate()

        self.f_x += self.change_x
        self.f_y += self.change_y
        self.rect.x = self.f_x
        self.rect.y = self.f_y

        for monster in self.player.game.check_collision(self, self.player.game.all_monster):
            self.remove()
            monster.damage(self.player.attack)

        if self.rect.x > 1080 or self.rect.y > 720:
            self.remove()
