import pygame
from pygame.sprite import Sprite
import math
import random
import math


class Zombie(Sprite):
    """
    Zombie class

    """

    def __init__(self, game_settings, screen, player):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.player = player

        # starting position of zombie, determined by calling random_spawn_generator()
        self.start_x = None
        self.start_y = None
        self.random_spawn_generator()

        # load zombie image and initial rect
        self.image = pygame.image.load("img/zombie.jpg")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.start_x
        self.rect.centery = self.start_y

        # create another pair of image and rect for rotated version, and update them
        self.rotated_image = pygame.image.load("img/zombie.jpg")
        self.updated_rect = self.rotated_image.get_rect()
        self.angle = None
        self.update()

    def random_spawn_generator(self):
        """
        Generates a random coordinate used as starting position of zombie
        :return: None (starting position is written into class attribute)
        """
        region_code = random.randint(1, 4)  # corresponds to four edges

        # create alias
        d = self.game_settings.spawn_distance
        s_h = self.game_settings.screen_height
        s_w = self.game_settings.screen_width

        # generate random coordinate
        if region_code == 1:  # spawn at left edge
            self.start_x = random.randint(-2 * d, -d)
            self.start_y = random.randint(0, s_h)
        elif region_code == 2:
            self.start_x = random.randint(0, s_w)
            self.start_y = random.randint(-2 * d, -d)
        elif region_code == 3:
            self.start_x = random.randint(s_w + d, s_w + 2 * d)
            self.start_y = random.randint(0, s_h)
        else:
            self.start_x = random.randint(0, s_w)
            self.start_y = random.randint(s_h + d, s_h + 2 * d)

    def update(self):
        """
        This method will do following:
            1. update the rotation angle of zombie, so it faces player
            2. update the coordinate of zombie's rect
        :return:
        """

        # calculate rotate angle and get rect
        # get player's position, used as "mouse position" as in player's class
        player_position = self.player.rect.centerx, self.player.rect.centery

        # calculate angle using the initial rect
        self.angle = math.degrees(math.atan2(self.rect.centery - player_position[1], self.rect.centerx - player_position[0]))

        # rotate zombie's image surface
        self.rotated_image = pygame.transform.rotate(self.image, 180 - self.angle)

        # find out where to blit the rotated image
        self.updated_rect = self.rotated_image.get_rect()  # get_rect() should be recalled to get the new rect as image rotates
        self.updated_rect.centerx = self.rect.centerx
        self.updated_rect.centery = self.rect.centery

        # update position (moving zombie)
        self.rect.centerx -= math.cos(math.radians(self.angle)) * self.game_settings.zombie_speed
        self.rect.centery -= math.sin(math.radians(self.angle)) * self.game_settings.zombie_speed

    def blit_zombie(self):
        """
        Blit the zombie to the screen
        """
        self.screen.blit(self.rotated_image, self.updated_rect)