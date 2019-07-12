import pygame
from pygame.sprite import Sprite
import math  # to calculate rotated angle


class BulletPistol(Sprite):
    """
    A class to manage bullets fired by player_pistol.

    Using similar idea in the alien invasion example
    """

    def __init__(self, game_settings, screen, player):
        """
        Create a bullet object at the player's pistol position
        (need player's position and mouse rotation info to determine final position)

        Parameters:
            game_settings: an object of Settings class, will use bullet setting inside

            screen: screen onto which the bullet will be drawn

            player: the player's character object, used to determine the position of the bullet

        """

        super().__init__()
        self.screen = screen  # used to draw Bullet on main screen
        self.game_settings = game_settings

        # calculate current rotate angle
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_position[1] - (player.updated_rect[1] + player.rect.width / 2),
                                mouse_position[0] - (player.updated_rect[0] + player.rect.height / 2))

        # load bullet image and make rotated image
        self.image = pygame.image.load("img/bullet_pistol.jpg")
        self.rotated_image = pygame.transform.rotate(self.image, 360 - self.angle * 57.29)

        # create a rect
        # self.rect = self.rotated_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = player.updated_rect[0] + player.rect.width / 2
        self.rect.centery = player.updated_rect[1] + player.rect.height / 2

    def update(self):
        """
        Update the bullet's position
        This is related to the rotated angle of the bullet
        """
        self.rect.centerx += math.cos(self.angle) * self.game_settings.bullet_pistol_speed
        self.rect.centery += math.sin(self.angle) * self.game_settings.bullet_pistol_speed

    def blit_bullet(self):
        """
        Blit the bullet to the screen
        """
        self.screen.blit(self.rotated_image, self.rect)