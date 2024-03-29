import pygame
from pygame.sprite import Sprite
import random
import math
from setting import Settings


class Zombie(Sprite):
    """
    Zombie class

    """
    # load zombie death resources as class variable to improve performance
    # images are stored separately for rotation purpose (sprite sheet does not help)
    pygame.mixer.pre_init(44100, -16, 1, 2048)
    pygame.init()
    death_images = []
    game_settings = Settings()
    zombie_death_sheet = game_settings.zombie_death_sheet_3

    # load last frame of corpse (this frame is displayed longer)
    for i in range(game_settings.zombie_corpse_display_frame):
        death_images.append(pygame.image.load(zombie_death_sheet[0]))
    # load previous death frame
    for i in range(len(zombie_death_sheet)):
        for j in range(game_settings.zombie_death_frame_multiplier):
            death_images.append(pygame.image.load(zombie_death_sheet[i]))

    # load sound effect
    zombie_attack_sound = []
    for i in range(len(game_settings.zombie_attack_sound_path)):
        zombie_attack_sound.append(pygame.mixer.Sound(game_settings.zombie_attack_sound_path[i]))

    zombie_hit_sound = pygame.mixer.Sound(game_settings.zombie_hit_sound_path)
    zombie_death_sound = pygame.mixer.Sound(game_settings.zombie_death_sound_path)

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
        self.image = pygame.image.load(game_settings.zombie_image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.start_x
        self.rect.centery = self.start_y

        # load zombie attack resources
        self.attack_image = pygame.image.load(self.game_settings.zombie_attack_image_path)
        self.attack_angle = 0

        # create sound channels
        self.attack_channel = pygame.mixer.Channel(game_settings.zombie_attack_channel)
        self.hit_channel = pygame.mixer.Channel(game_settings.zombie_hit_channel)

        # create another pair of image and rect for rotated version, and update them
        self.rotated_image = pygame.image.load(game_settings.zombie_image_path)
        self.updated_rect = self.rotated_image.get_rect()
        self.angle = None

        # record the time of last attacking
        self.last_attacking_time = 0

        # zombie health and zombie hit slow down factor
        self.hp = self.game_settings.zombie_max_health
        self.hit_slow_down_factor = 1  # ratio multiplied to speed, will be modified when hit by a certain kinds of bullet, will restore over time

        # initialize update
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
            1. update zombie coordinate and orientation
        :return:
        """

        # update zombie's position
        self.update_zombie_pos()

        # update slow down factor
        if self.hit_slow_down_factor < 1:
            self.hit_slow_down_factor += self.game_settings.zombie_hit_slow_down_restore_factor

    def update_zombie_pos(self):
        # calculate rotate angle and get rect
        # get player's position, used as "mouse position" as in player's class
        player_position = self.player.rect.centerx, self.player.rect.centery

        # calculate angle using the initial rect
        self.angle = math.degrees(
            math.atan2(self.rect.centery - player_position[1], self.rect.centerx - player_position[0]))

        # rotate zombie's image surface
        # use attack_image if zombie just attacked
        if self.attack_angle != 0:
            self.rotated_image = pygame.transform.rotate(self.attack_image, 180 - self.angle + self.attack_angle)
            self.attack_angle -= 1
        else:
            self.rotated_image = pygame.transform.rotate(self.image, 180 - self.angle)

        # find out where to blit the rotated image
        self.updated_rect = self.rotated_image.get_rect()  # get_rect() should be recalled to get the new rect as image rotates
        self.updated_rect.centerx = self.rect.centerx
        self.updated_rect.centery = self.rect.centery

        # update position (moving zombie)
        self.rect.centerx -= math.cos(math.radians(self.angle)) * self.game_settings.zombie_speed * self.hit_slow_down_factor
        self.rect.centery -= math.sin(math.radians(self.angle)) * self.game_settings.zombie_speed * self.hit_slow_down_factor

    def attack_player(self, player):
        """
        This function is called when player's rect and zombie's rect collide
        -display attacking animation (?)
        -play attack sound
        -subtract player's hp
        -update last attacked time

        :return:
        """

        # set attack angle, so zombie will show a sweep animation
        self.attack_angle = 45

        # subtract player's health
        damage = random.randint(1, self.game_settings.zombie_damage)
        player.hp -= damage

        # update last attack time
        self.last_attacking_time = pygame.time.get_ticks()

        # play random attack sound
        self.attack_channel.play(self.zombie_attack_sound[random.randint(0, len(self.game_settings.zombie_attack_sound_path) - 1)])

    def blit_zombie(self):
        """
        Blit the zombie to the screen, and its health bar
        """
        self.screen.blit(self.rotated_image, self.updated_rect)

        # draw health bar above zombie: health bar box and health bar
        pygame.draw.rect(self.screen, (0, 0, 0), (self.rect[0] + 35, self.rect[1] - 5, self.game_settings.zombie_max_health_bar_length, 10), 1)
        pygame.draw.rect(self.screen, self.game_settings.DARK_GREEN, (self.rect[0] + 36, self.rect[1] - 4, int(self.hp / self.game_settings.zombie_max_health * self.game_settings.zombie_max_health_bar_length) - 1, 8))


class DeadZombie(Sprite):
    """
    This class is used to draw the dead zombie animation
    """

    def __init__(self, zombie):
        # initialiation of base class (Sprite)
        super().__init__()

        # get the rotated angle and position of current zombie
        # get the display screen from current zombie
        self.angle = zombie.angle
        self.rect = zombie.rect
        self.screen = zombie.screen
        self.game_settings = zombie.game_settings
        self.zombie_death_sheet = zombie.zombie_death_sheet
        self.death_images = zombie.death_images[:]

    def blit_death_frame(self):
        """
        Blit one frame of death image from the self.death_images
        Then delete one frame
        (The dead_zombie object will be deleted from dead_zombies sprite group is death_images is empty: no need to display any more)
        :return:
        """
        rotated_image = pygame.transform.rotate(self.death_images[-1], 180 - self.angle)
        # self.screen.blit(rotated_image, (self.rect[0] - 22, self.rect[1] - 19, self.rect[2] * 2, self.rect[3] * 2))
        self.screen.blit(rotated_image, self.rect)
        # print('zombie rect (x, y):', self.rect)

    def update(self):
        # remove the last frame
        self.death_images.pop()
