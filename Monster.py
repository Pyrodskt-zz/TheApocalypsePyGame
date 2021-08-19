import random

import pygame


class Monster(pygame.sprite.Sprite):

    def __init__(self, game):
        # init the parent class --> Sprite
        # define that this it gonna be a sprite object
        super().__init__()
        # inherit game object to access its functions and parameters
        self.game = game
        # max health possible to have
        self.maxhealth = 100
        # init the monster with the max health
        self.health = self.maxhealth
        # value of attack if more ... you will die instantly ... not very funny
        self.attack = 0.3

        # load img of monster and convert to alpha
        self.image = pygame.image.load('assets/mummy.png').convert_alpha()

        # get rectangle of the img to be able to handle interactions
        self.rect = self.image.get_rect()

        # random number between 0 and 1, to make the monster spawn on the left side or the right side
        self.randx = random.randint(0, 1)

        # make the monster spawn on the side depending on randx with random coordinates between 2 values like this
        # monsters don't spawn on the same position
        if self.randx:
            self.rect.x = random.randrange(800, 1000, step=100)
        else:
            self.rect.x = random.randrange(100, 300, step=100)


        # y position is constant --> same of the player
        self.rect.y = 540

        # random velocity
        self.velocity = random.randrange(1, 5)

    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 12, self.rect.y - 20, self.maxhealth, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 12, self.rect.y - 20, self.health, 5])

    def damage(self, amount):
        self.health -= amount
        # if health under 0 kill the monster and change linked values
        if self.health <= 0:
            self.kill()
            self.game.score += 1
            self.game.monsters_in_screen -=1

    def forward(self):
        # auto move forward depending player position
        # check if collision with player

        if not self.game.check_collision(self, self.game.all_player):
            if self.game.player.rect.x < self.rect.x:
                self.rect.x -= self.velocity
            else:
                self.rect.x += self.velocity
        # if collision with player put damage to player
        else:
            self.game.player.damage(self.attack)