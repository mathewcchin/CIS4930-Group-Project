import pygame
from pygame.sprite import Sprite
import math  # to calculate rotated angle
import copy
import random


class BulletM4(Sprite):
    """
    A class to manage bullets fired by m4.

    """

    def __init__(self, game_settings, screen, player):
        """
        Create a m4 bullet object at the player's m4 position
        (need player's position and mouse rotation info to determine final position)

        Parameters:
            game_settings: an object of Settings class, will use bullet setting inside

            screen: screen onto which the bullet will be drawn

            player: the player's character object, used to determine the position of the bullet

        """

        super().__init__()
        self.screen = screen  # used to draw Bullet on main screen
        self.game_settings = game_settings
        self.bullet_type = self.game_settings.m4

        # get current rotate angle
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_position[1] - (player.updated_rect[1] + player.rect.width / 2),
                                mouse_position[0] - (player.updated_rect[0] + player.rect.height / 2))

        self.angle_got = copy.copy(player.angle)

        # load bullet image and make rotated image
        self.image = pygame.image.load(self.game_settings.bullet_m4_image_path)
        self.rotated_image = pygame.transform.rotate(self.image, 360 - math.degrees(self.angle))

        # create a rect
        self.rect = self.rotated_image.get_rect()

        # calculate the position to put the initialized bullet
        # 36 and 32 are results of trial and error
        self.rect.centerx = player.rect[0] + 40 * math.sin(math.radians(90) - self.angle) + 36
        self.rect.centery = player.rect[1] + 40 * math.cos(math.radians(90) - self.angle) + 32

        # bullet travel distance count
        self.traveled_distance = 0

        # bullet damage
        self.damage = random.randint(self.game_settings.bullet_m4_min_damage,
                                     self.game_settings.bullet_m4_max_damage)
        self.original_damage = self.damage

        # bullet slow down factor
        self.slow_down_factor = self.game_settings.bullet_m4_slow_down_factor


    def update(self):
        """
        Update the bullet's position and record the total traveled distance
        This is related to the rotated angle of the bullet
        """
        self.rect.centerx += math.cos(self.angle) * self.game_settings.bullet_m4_speed
        self.rect.centery += math.sin(self.angle) * self.game_settings.bullet_m4_speed

        # update traveled distance
        self.traveled_distance += self.game_settings.bullet_m4_speed

    def blit_bullet(self):
        """
        Blit the bullet to the screen
        """
        self.screen.blit(self.rotated_image, self.rect)


class BulletPistol(Sprite):
    """
    A class to manage bullets fired by pistol.

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
        self.bullet_type = self.game_settings.pistol

        # get current rotate angle
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_position[1] - (player.updated_rect[1] + player.rect.width / 2),
                                mouse_position[0] - (player.updated_rect[0] + player.rect.height / 2))

        self.angle_got = copy.copy(player.angle)

        # load bullet image and make rotated image
        self.image = pygame.image.load(self.game_settings.bullet_pistol_image_path)
        self.rotated_image = pygame.transform.rotate(self.image, 360 - math.degrees(self.angle))

        # create a rect
        self.rect = self.rotated_image.get_rect()

        # calculate the position to put the initialized bullet
        # 36 and 32 are results of trial and error
        self.rect.centerx = player.rect[0] + 40 * math.sin(math.radians(90) - self.angle) + 36
        self.rect.centery = player.rect[1] + 40 * math.cos(math.radians(90) - self.angle) + 32

        # bullet travel distance count
        self.traveled_distance = 0

        # bullet damage
        self.damage = random.randint(self.game_settings.bullet_pistol_min_damage,
                                     self.game_settings.bullet_pistol_max_damage)
        self.original_damage = self.damage

        # bullet slow down factor
        self.slow_down_factor = self.game_settings.bullet_pistol_slow_down_factor

    def update(self):
        """
        Update the bullet's position and record the total traveled distance
        This is related to the rotated angle of the bullet
        """
        self.rect.centerx += math.cos(self.angle) * self.game_settings.bullet_pistol_speed
        self.rect.centery += math.sin(self.angle) * self.game_settings.bullet_pistol_speed

        # update traveled distance
        self.traveled_distance += self.game_settings.bullet_pistol_speed

    def blit_bullet(self):
        """
        Blit the bullet to the screen
        """
        self.screen.blit(self.rotated_image, self.rect)


class BulletAwp(Sprite):
    """
    A class to manage bullets fired by m4.

    """

    def __init__(self, game_settings, screen, player):
        """
        Create a awp bullet object at the player's awp position
        (need player's position and mouse rotation info to determine final position)

        Parameters:
            game_settings: an object of Settings class, will use bullet setting inside

            screen: screen onto which the bullet will be drawn

            player: the player's character object, used to determine the position of the bullet

        """

        super().__init__()
        self.screen = screen  # used to draw Bullet on main screen
        self.game_settings = game_settings
        self.bullet_type = self.game_settings.awp

        # get current rotate angle
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_position[1] - (player.updated_rect[1] + player.rect.width / 2),
                                mouse_position[0] - (player.updated_rect[0] + player.rect.height / 2))

        self.angle_got = copy.copy(player.angle)

        # load bullet image and make rotated image
        self.image = pygame.image.load(self.game_settings.bullet_awp_image_path)
        self.rotated_image = pygame.transform.rotate(self.image, 360 - math.degrees(self.angle))

        # create a rect
        self.rect = self.rotated_image.get_rect()

        # calculate the position to put the initialized bullet
        # 36 and 32 are results of trial and error
        self.rect.centerx = player.rect[0] + 40 * math.sin(math.radians(90) - self.angle) + 36
        self.rect.centery = player.rect[1] + 40 * math.cos(math.radians(90) - self.angle) + 32

        # bullet travel distance count
        self.traveled_distance = 0

        # bullet damage
        self.damage = random.randint(self.game_settings.bullet_awp_min_damage,
                                     self.game_settings.bullet_awp_max_damage)
        self.original_damage = self.damage

        # bullet slow down factor
        self.slow_down_factor = self.game_settings.bullet_awp_slow_down_factor

    def update(self):
        """
        Update the bullet's position and record the total traveled distance
        This is related to the rotated angle of the bullet
        """
        self.rect.centerx += math.cos(self.angle) * self.game_settings.bullet_awp_speed
        self.rect.centery += math.sin(self.angle) * self.game_settings.bullet_awp_speed

        # update traveled distance
        self.traveled_distance += self.game_settings.bullet_awp_speed

    def blit_bullet(self):
        """
        Blit the bullet to the screen
        """
        self.screen.blit(self.rotated_image, self.rect)