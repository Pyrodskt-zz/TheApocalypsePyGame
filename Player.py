import math

import pygame
from Projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        # init parent class
        # define that object is gonna be a sprite object
        super().__init__()
        # inherit game object to access its functions and parameters
        self.game = game

        # set max health possible to have
        self.maxhealth = 100
        self.health = self.maxhealth

        # set attack of the player --> 1 shoot monster
        self.attack = 100

        # set player is not jumping
        self.isJumping = False

        # set max height of jump
        self.jumpCount = 10

        # set velocity of player
        self.velocity = 8

        # load image, resize and make rectangle to handle interactions
        self.cursor_img = pygame.image.load('assets/Crosshairs/Crosshair11_hit.png').convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (50, 50))
        self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_img_origin = self.cursor_img.copy()

        # angle use for cursor rotation
        self.angle = 0

        # load cursor img, resize it, make rectangle to handle interactions
        self.cursor_img_rect.x, self.cursor_img_rect.y = pygame.mouse.get_pos()

        # create sprite group for projectiles to get the sprites group methods like draw
        self.all_projectiles = pygame.sprite.Group()

        # load player img, place it to its origin position
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 500
        self.y_origin = 500

        # set the fire rate, not used currently
        self.fire_rate = 1

    def lauch_projectile(self):
        # lauch projectile to the mouse coordinates
        # calculate the trajectory and pass it in parameters
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # adjust the distance because of the player img size and the start point of the projectile --> right arm
        distance_x = (mouse_x - self.rect.x) - 145
        distance_y = (mouse_y - self.rect.y) - 105
        angle = math.atan2(distance_y, distance_x)
        # after calculation add the projectile to the sprite group with the good angle
        self.all_projectiles.add(Projectile(self, angle))

    def update_health_bar(self, surface):
        # update player health bar
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 45, self.rect.y, self.maxhealth, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 45, self.rect.y, self.health, 5])

    def damage(self, amount):
        # if player is taking damage
        # if health equal 0 game over
        if self.health - amount > amount:
            self.health -= amount
        else:
            self.game.game_over()

    # cursor rotation to bring some movements in the screen
    def rotate_cursor(self):
        # cursor image rotation speed
        self.angle += 0.5 % 360
        # set the rotation using the center of the cursor image not the top left corner
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img_origin, self.angle, 1)
        self.cursor_img_rect.center = self.cursor_img.get_rect().center

    # moving functions, check if not collide a monster
    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monster):
            self.rect.x += self.velocity

    def move_left(self):
        if not self.game.check_collision(self, self.game.all_monster):
            self.rect.x -= self.velocity

    def jump(self):
        # Check if player is jumping and then execute the
        # jumping code.
        # making a jump moving like a parabola
        if self.isJumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    # if player reached max jump height make it go down
                    neg = -1
                self.rect.y -= (self.jumpCount ** 2) * 0.4 * neg
                self.jumpCount -= 1
            else:
                # if player back to origin position reset the values
                # may put error of +/- 5px check in main there is 2 if statements to correct the pb
                self.isJumping = False
                self.jumpCount = 10