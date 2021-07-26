import math

import pygame
from Projectile import Projectile



class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.maxhealth = 100
        self.attack = 25
        self.isJumping = False
        self.jumpCount = 10
        self.velocity = 8
        self.cursor_img = pygame.image.load('assets/Crosshairs/Crosshair11_hit.png').convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (50, 50))
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_img_origin = self.cursor_img.copy()
        self.angle = 0

        self.cursor_img_rect.x, self.cursor_img_rect.y = pygame.mouse.get_pos()
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 500
        self.y_origin = 500

    def lauch_projectile(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        distance_x = (mouse_x - self.rect.x) - 145
        distance_y = (mouse_y - self.rect.y) - 105
        angle = math.atan2(distance_y, distance_x)
        self.all_projectiles.add(Projectile(self, angle))

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 45, self.rect.y, self.maxhealth, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 45, self.rect.y, self.health, 5])

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount

    def rotate_cursor(self):
        # cursor image rotation speed
        self.angle += 0.5 % 360
        # set the rotation using the center of the cursor image not the top left corner
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img_origin, self.angle, 1)
        self.cursor_img_rect.center = self.cursor_img.get_rect().center

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monster):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def jump(self):
        # Check if mario is jumping and then execute the
        # jumping code.
        if self.isJumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect.y -= (self.jumpCount ** 2) * 0.4 * neg
                print(self.rect.y)
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = 10