import pygame
import random  # for playing foot steps randomly
import math  # for calculating rotated angle
import game_functions as gf


class PlayerPistol:
    """
    This class is the default player's character class (holding a pistol)

    Attributes (self.):

    """

    def __init__(self, screen, game_settings):
        """
        Initialization of Player class

        Parameters:
            :screen: this is the surface where the character will be drawn
            :game_settings: containing character settings
        """

        # set screen and game_settings
        self.screen = screen
        self.game_settings = game_settings

        # load character image and get its rect
        self.image = pygame.image.load('img/player_pistol.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # get player rotation 
        mouse_position = pygame.mouse.get_pos()      
        self.angle = math.atan2(self.rect.centery - mouse_position[1], self.rect.centerx - mouse_position[0]) * 57.29
        
        # set player's starting position (center of the screen)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # character foot step sound effect
        self.foot_step_sound_1 = pygame.mixer.Sound('sfx/character/pl_step1.wav')
        self.foot_step_sound_2 = pygame.mixer.Sound('sfx/character/pl_step2.wav')
        self.foot_step_sound_3 = pygame.mixer.Sound('sfx/character/pl_step3.wav')
        self.foot_step_sound_4 = pygame.mixer.Sound('sfx/character/pl_step4.wav')
        # create a tuple to hold the sound of foot steps
        self.foot_steps = self.foot_step_sound_1, self.foot_step_sound_2, self.foot_step_sound_3, self.foot_step_sound_4
        # create a channel for playing foot step sounds
        self.foot_steps_channel = pygame.mixer.Channel(game_settings.foot_step_channel)

        # character moving flag, if the flag is true, character should be in a continuously moving state
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        # record the time of last shooting
        self.last_shooting_time = 0

        # record the number of enemies killed, number of shots
        self.zombie_killed = 0
        self.shots = 0
        self.accuracy = 0

        # player health point
        self.heart_image = pygame.image.load('img/heart.png')
        self.hp = self.game_settings.max_health_point

        # load ammo and fire resources and set attributes
        self.ammo_pistol = self.game_settings.initial_pistol_ammo
        self.clip_pistol = self.game_settings.pistol_clip_capacity
        self.pistol_sound = pygame.mixer.Sound(self.game_settings.pistol_sound_path)
        self.ammo_pickup_sound = pygame.mixer.Sound(self.game_settings.ammo_pickup_sound_path)
        self.clip_empty_sound = pygame.mixer.Sound(self.game_settings.clip_empty_sound_path)
        self.clip_change_sound = pygame.mixer.Sound(self.game_settings.clip_change_sound_path)
        self.item_pickup_sound = pygame.mixer.Sound(self.game_settings.item_pickup_sound_path)
        self.pisto_channel = pygame.mixer.Channel(self.game_settings.pistol_channel)

        self.fire_image = pygame.image.load('img/player_pistol_fire.jpg')

        self.pistol_reload_frame = 0


    def update(self):
        """
        This method will do following:
            1. update the coordinate of player's rect 
            2. play foot step if player is moving
            3. update the rotation of player's image
            
        """

        # play foot step
        self.play_foot_step()

        # update player's coordinate and orientation
        self.update_player_pos()

        # count reload time and reload
        self.count_reload_time()

    def play_foot_step(self):
        # play random foot step sound while moving flag is true
        # if the character is trying to move out of the boundary, don't play sound
        if (self.moving_down and self.rect.bottom + self.game_settings.allowed_margin < self.screen_rect.bottom) or (
                self.moving_left and self.rect.left > self.game_settings.allowed_margin) or (
                self.moving_right and self.rect.right + self.game_settings.allowed_margin < self.screen_rect.right) or (
                self.moving_up and self.rect.top > self.game_settings.allowed_margin):
            if not self.foot_steps_channel.get_busy():  # if foot step channel is not playing
                self.foot_steps_channel.play(self.foot_steps[random.randint(0, 3)])

        # stop playing sound effect when player stopped
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.foot_steps_channel.stop()

    def update_player_pos(self):
        # update player's coordinate, bound player within the screen
        if self.moving_down and self.rect.bottom + self.game_settings.allowed_margin < self.screen_rect.bottom:
            self.rect.centery += self.game_settings.character_speed

        if self.moving_left and self.rect.left > self.game_settings.allowed_margin:
            self.rect.centerx -= self.game_settings.character_speed

        if self.moving_right and self.rect.right + self.game_settings.allowed_margin < self.screen_rect.right:
            self.rect.centerx += self.game_settings.character_speed

        if self.moving_up and self.rect.top > self.game_settings.allowed_margin:
            self.rect.centery -= self.game_settings.character_speed

        # rotate player's image
        # get mouse coordinate
        mouse_position = pygame.mouse.get_pos()

        # calculate angle using the initial rect
        self.angle = math.degrees(
            math.atan2(self.rect.centery - mouse_position[1], self.rect.centerx - mouse_position[0]))

        # rotate player's image surface and store rotated image in player's object
        self.rotated_image = pygame.transform.rotate(self.image, 180 - self.angle)

        # find out where to blit the rotated image (coordinate of the upper left corner), store the updated rect in player's object
        self.updated_rect = self.rotated_image.get_rect()
        self.updated_rect.centerx = self.rect.centerx
        self.updated_rect.centery = self.rect.centery

    def count_reload_time(self):
        # count reload time if self.pistol_reload_frame is not zero
        # this means the player is reloading
        # update player's clip number when self.pistol_reload_frame is returned to zero
        if self.pistol_reload_frame > 0:
            self.pistol_reload_frame -= 1
            if self.pistol_reload_frame == 0:
                self.ammo_pistol += self.clip_pistol  # get remainning ammo
                if self.ammo_pistol > self.game_settings.pistol_clip_capacity:
                    self.clip_pistol = self.game_settings.pistol_clip_capacity
                    self.ammo_pistol -= self.game_settings.pistol_clip_capacity
                else:
                    self.clip_pistol = self.ammo_pistol
                    self.ammo_pistol = 0

    def display_firing(self):
        # play the shooting sound at designated channel
        self.pisto_channel.play(self.pistol_sound)

        # rotate the fire image according to current mouse position
        rotated_fire_image = pygame.transform.rotate(self.fire_image, 180 - self.angle)

        # blit and show the fire frame
        for i in range(30):
            self.screen.blit(rotated_fire_image, self.updated_rect)
            pygame.display.flip()

        # update shooting time
        self.last_shooting_time = pygame.time.get_ticks()

        # update clip
        self.clip_pistol -= 1

    def injured(self):
        """
        This function is called when player is being attacked by zombie
        -play injury sound
        -
        :return:
        """
        pass

    def reload(self):
        """
        Reload clip
        :return:
        """
        self.pistol_reload_frame = self.game_settings.pistol_reload_speed
        self.pisto_channel.play(self.clip_change_sound)

    def blit_player(self):
        """
        This function will:
            - draw player
            - draw health bar
            - display ammo amount
            - draw reload bar if player is reloading
        :return:
        """
        # draw player, called in update_screen() function
        self.screen.blit(self.rotated_image, self.updated_rect)

        # draw health bar
        self.screen.blit(self.heart_image, (1000, 730))  # draw heart
        pygame.draw.rect(self.screen, (0, 0, 0), (1030, 730, self.game_settings.max_health_bar_length, 20), 1)  # draw hp box
        pygame.draw.rect(self.screen, (255, 0, 0), (1031, 731, int(self.game_settings.max_health_bar_length * self.hp / self.game_settings.max_health_point), 18))

        # display ammo amount
        ammo_text_surface = gf.text_format(str(self.clip_pistol) + '/' + str(self.ammo_pistol), self.game_settings.digital_font_path, 40, (255, 230, 140))
        self.screen.blit(ammo_text_surface, (850, 720))

        # draw reload progress bar if player is reloading
        if self.pistol_reload_frame > 0:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.rect[0], self.rect[1] - 30, self.game_settings.max_reload_bar_length, 20), 1)
            pygame.draw.rect(self.screen, (255, 230, 140), (self.rect[0] - 1, self.rect[1] - 29, int(self.game_settings.max_reload_bar_length * (1 - self.pistol_reload_frame / self.game_settings.pistol_reload_speed)), 18))