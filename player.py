import pygame
import random  # for playing foot steps randomly
import math  # for calculating rotated angle
import game_functions as gf
from bullet import *


class Player:
    """
    This class is the default player's character class (holding a pistol)

    Attributes (self.):

    """

    def __init__(self, screen, game_settings, bullets, resources):
        """
        Initialization of Player class

        Parameters:
            :screen: this is the surface where the character will be drawn
            :game_settings: containing character settings
        """

        # set screen, game_settings and resources
        self.screen = screen
        self.game_settings = game_settings
        self.resources = resources

        # load character image and get its rect
        self.image = pygame.image.load(self.game_settings.player_pistol_image_path)  # will be used to rotate and display
        self.image_pistol = pygame.image.load(self.game_settings.player_pistol_image_path)
        self.image_m4 = pygame.image.load(self.game_settings.player_m4_image_path)
        self.image_awp = pygame.image.load(self.game_settings.player_awp_image_path)

        self.rect = self.image.get_rect()  # rect will be used to store moving info
        self.rect_pistol = self.image_pistol.get_rect()
        self.rect_m4 = self.image_m4.get_rect()
        self.rect_awp = self.image_awp.get_rect()
        self.screen_rect = screen.get_rect()

        # get player rotation 
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(self.rect.centery - mouse_position[1], self.rect.centerx - mouse_position[0]) * 57.29
        
        # set player's starting position (center of the screen)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        # character foot step sound effect
        self.last_foot_step_time = 0  # control foot step play interval
        self.foot_step_sound_1 = pygame.mixer.Sound(self.game_settings.foot_step_sound1_path)
        self.foot_step_sound_2 = pygame.mixer.Sound(self.game_settings.foot_step_sound2_path)
        self.foot_step_sound_3 = pygame.mixer.Sound(self.game_settings.foot_step_sound3_path)
        self.foot_step_sound_4 = pygame.mixer.Sound(self.game_settings.foot_step_sound4_path)
        # create a tuple to hold the sound of foot steps
        self.foot_steps = self.foot_step_sound_1, self.foot_step_sound_2, self.foot_step_sound_3, self.foot_step_sound_4
        # create a channel for playing foot step sounds
        self.foot_steps_channel = pygame.mixer.Channel(game_settings.foot_step_channel)

        # character moving flag, if the flag is true, character should be in a continuously moving state
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # record the number of enemies killed, number of shots
        self.zombie_hit = 0
        self.zombie_killed = 0
        self.shots = 0
        self.accuracy = 0

        # player health point
        self.heart_image = pygame.image.load(self.game_settings.player_health_icon_path)
        self.hp = self.game_settings.max_health_point

        # load ammo and fire resources and set attributes
        self.bullets = bullets  # Sprite class used to hold bullets

            # pistol
        self.ammo_pistol = self.game_settings.initial_pistol_ammo
        self.clip_pistol = self.game_settings.pistol_clip_capacity
        self.pistol_sound = pygame.mixer.Sound(self.game_settings.pistol_sound_path)
        self.pistol_image = pygame.image.load(self.game_settings.pistol_image_path)
            # automatic rifle
        self.ammo_m4 = self.game_settings.initial_m4_ammo
        self.clip_m4 = self.game_settings.m4_clip_capacity
        self.m4_sound = pygame.mixer.Sound(self.game_settings.m4_sound_path)
        self.m4_image = pygame.image.load(self.game_settings.m4_image_path)
            # awp
        self.ammo_awp = self.game_settings.initial_awp_ammo
        self.clip_awp = self.game_settings.awp_clip_capacity
        self.awp_sound = pygame.mixer.Sound(self.game_settings.awp_sound_path)
        self.awp_image = pygame.image.load(self.game_settings.awp_image_path)

        self.ammo_pickup_sound = pygame.mixer.Sound(self.game_settings.ammo_pickup_sound_path)
        self.clip_empty_sound = pygame.mixer.Sound(self.game_settings.clip_empty_sound_path)

        # reload sound
        self.pistol_reload_sound = pygame.mixer.Sound(self.game_settings.pistol_reload_sound_path)
        self.m4_reload_sound = pygame.mixer.Sound(self.game_settings.m4_reload_sound_path)
        self.awp_reload_sound = pygame.mixer.Sound(self.game_settings.awp_reload_sound_path)
        self.reload_sounds = (self.pistol_reload_sound, self.m4_reload_sound, self.awp_reload_sound)

        # item pickup sound
        self.item_pickup_sound = pygame.mixer.Sound(self.game_settings.item_pickup_sound_path)

        # define gun channel
        self.gun_channel = pygame.mixer.Channel(self.game_settings.gun_channel)

        self.reload_frame = 0
        self.auto_reload_flag = False

        self.last_pistol_shooting_time = 0
        self.last_auto_shooting_time = 0
        self.last_awp_shooting_time = 0

        # weapon carrying initially
        self.current_weapon = self.game_settings.pistol
        self.auto_shooting = False

        # fire sheets container, will be filled by data in self.resources when fire
        # these images have higher precedence than normal player image to blit
        self.pistol_fire_sheet = []
        self.m4_fire_sheet = []
        self.awp_fire_sheet = []

    def update(self):
        """
        This method will do following:
            1. update the coordinate of player's rect 
            2. play foot step if player is moving
            3. update the rotation of player's image
            
        """
        # update player's image according to different weapons carrying
        if self.current_weapon == self.game_settings.pistol:
            self.image = self.image_pistol
        elif self.current_weapon == self.game_settings.m4:
            self.image = self.image_m4
        elif self.current_weapon == self.game_settings.awp:
            self.image = self.image_awp

        # play foot step
        self.play_foot_step()

        # update player's coordinate and orientation
        self.update_player_pos()

        # count reload time and reload
        self.count_reload_time()

        # check auto weapon fire and reload
        if self.current_weapon == self.game_settings.m4 and self.auto_shooting:
            self.m4_fire()

        if self.clip_m4 == 0 and self.auto_reload_flag and self.reload_frame == 0 and self.ammo_m4 > 0:
            self.reload_frame = self.game_settings.m4_reload_speed
            self.gun_channel.play(self.m4_reload_sound)

    def play_foot_step(self):
        # play random foot step sound while moving flag is true
        # if the character is trying to move out of the boundary, don't play sound
        if (self.moving_down and self.rect.bottom + self.game_settings.allowed_margin < self.screen_rect.bottom) or (
                self.moving_left and self.rect.left > self.game_settings.allowed_margin) or (
                self.moving_right and self.rect.right + self.game_settings.allowed_margin < self.screen_rect.right) or (
                self.moving_up and self.rect.top > self.game_settings.allowed_margin):
            # if not self.foot_steps_channel.get_busy():  # if foot step channel is not playing
            if pygame.time.get_ticks() - self.last_foot_step_time >= self.game_settings.weapon_foot_step_interval[self.current_weapon]:
                self.foot_steps_channel.play(self.foot_steps[random.randint(0, 3)])
                self.last_foot_step_time = pygame.time.get_ticks()

        # stop playing sound effect when player stopped
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.foot_steps_channel.stop()

    def update_player_pos(self):
        # update player's coordinate, bound player within the screen
        if self.moving_down and self.rect.bottom + self.game_settings.allowed_margin < self.screen_rect.bottom:
            self.rect.centery += self.game_settings.character_speed - self.game_settings.weapon_speed_reduce_factor[self.current_weapon]

        if self.moving_left and self.rect.left > self.game_settings.allowed_margin:
            self.rect.centerx -= self.game_settings.character_speed - self.game_settings.weapon_speed_reduce_factor[self.current_weapon]

        if self.moving_right and self.rect.right + self.game_settings.allowed_margin < self.screen_rect.right:
            self.rect.centerx += self.game_settings.character_speed - self.game_settings.weapon_speed_reduce_factor[self.current_weapon]

        if self.moving_up and self.rect.top > self.game_settings.allowed_margin:
            self.rect.centery -= self.game_settings.character_speed - self.game_settings.weapon_speed_reduce_factor[self.current_weapon]

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
        if self.reload_frame > 0:
            self.reload_frame -= 1
            if self.reload_frame == 0:
                if self.current_weapon == self.game_settings.pistol:
                    self.reload_pistol()
                if self.current_weapon == self.game_settings.m4:
                    self.reload_m4()
                if self.current_weapon == self.game_settings.awp:
                    self.reload_awp()

    def reload_pistol(self):
        self.ammo_pistol += self.clip_pistol  # get remainning ammo
        if self.ammo_pistol > self.game_settings.pistol_clip_capacity:
            self.clip_pistol = self.game_settings.pistol_clip_capacity
            self.ammo_pistol -= self.game_settings.pistol_clip_capacity
        else:
            self.clip_pistol = self.ammo_pistol
            self.ammo_pistol = 0

        self.auto_reload_flag = False

    def reload_m4(self):
        self.ammo_m4 += self.clip_m4  # get remainning ammo
        if self.ammo_m4 > self.game_settings.m4_clip_capacity:
            self.clip_m4 = self.game_settings.m4_clip_capacity
            self.ammo_m4 -= self.game_settings.m4_clip_capacity
        else:
            self.clip_m4 = self.ammo_m4
            self.ammo_m4 = 0

        self.auto_reload_flag = False

    def reload_awp(self):
        self.ammo_awp += self.clip_awp  # get remainning ammo
        if self.ammo_awp > self.game_settings.awp_clip_capacity:
            self.clip_awp = self.game_settings.awp_clip_capacity
            self.ammo_awp -= self.game_settings.awp_clip_capacity
        else:
            self.clip_awp = self.ammo_awp
            self.ammo_awp = 0

        self.auto_reload_flag = False

    def fire(self):
        # check current weapon
        if self.current_weapon == self.game_settings.pistol:
            self.pistol_fire()  # fire directly

        elif self.current_weapon == self.game_settings.m4:
            self.auto_shooting = True
            self.auto_reload_flag = False

        elif self.current_weapon == self.game_settings.awp:
            self.awp_fire()  # fire directly

    def pistol_fire(self):
        if pygame.time.get_ticks() - self.last_pistol_shooting_time >= self.game_settings.pistol_shooting_interval and not gf.is_mouse_in_player(
                self) and self.reload_frame == 0:
            if self.clip_pistol > 0:
                # create a pistol bullet and add to bullets
                new_bullet = BulletPistol(self.game_settings, self.screen, self)
                self.bullets.add(new_bullet)
                self.shots += 1  # add to total number of shots
                self.accuracy = self.zombie_hit / self.shots  # update accuracy

                # play the shooting sound at designated channel
                self.gun_channel.play(self.pistol_sound)

                # # blit and show the fire frame
                # for i in range(30):
                #     self.screen.blit(rotated_fire_image, self.updated_rect)
                #     pygame.display.flip()

                # set pistol fire sheet
                self.pistol_fire_sheet = self.resources.pistol_fire_sheet[:]

                # update shooting time
                self.last_pistol_shooting_time = pygame.time.get_ticks()

                # update clip
                self.clip_pistol -= 1

            else:
                self.gun_channel.play(self.clip_empty_sound)
                if self.ammo_pistol > 0:
                    self.reload()

    def awp_fire(self):
        if pygame.time.get_ticks() - self.last_awp_shooting_time >= self.game_settings.awp_shooting_interval and not gf.is_mouse_in_player(
                self) and self.reload_frame == 0:
            if self.clip_awp > 0:
                # create a awp bullet and add to bullets
                new_bullet = BulletAwp(self.game_settings, self.screen, self)
                self.bullets.add(new_bullet)
                self.shots += 1  # add to total number of shots
                self.accuracy = self.zombie_hit / self.shots  # update accuracy

                # play the shooting sound at designated channel
                self.gun_channel.play(self.awp_sound)

                # set awp fire sheet
                self.awp_fire_sheet = self.resources.awp_fire_sheet[:]

                # update shooting time
                self.last_awp_shooting_time = pygame.time.get_ticks()

                # update clip
                self.clip_awp -= 1

            else:
                self.gun_channel.play(self.clip_empty_sound)
                self.reload()

    def m4_fire(self):
        if pygame.time.get_ticks() - self.last_auto_shooting_time >= self.game_settings.m4_shooting_interval and not gf.is_mouse_in_player(
                self) and self.reload_frame == 0:

            # update shooting time
            self.last_auto_shooting_time = pygame.time.get_ticks()

            if self.clip_m4 > 0:
                # create a pistol bullet and add to bullets
                new_bullet = BulletM4(self.game_settings, self.screen, self)
                self.bullets.add(new_bullet)
                self.shots += 1  # add to total number of shots
                self.accuracy = self.zombie_hit / self.shots  # update accuracy

                # play the shooting sound at designated channel
                self.gun_channel.play(self.m4_sound)

                # set m4 fire sheet
                self.m4_fire_sheet = self.resources.m4_fire_sheet[:]

                # update clip
                self.clip_m4 -= 1

            else:
                self.gun_channel.play(self.clip_empty_sound)

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
        self.reload_frame = self.game_settings.reload_speed[self.current_weapon]
        self.gun_channel.play(self.reload_sounds[self.current_weapon])

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
        if self.pistol_fire_sheet:
            self.blit_pistol_fire()
        elif self.m4_fire_sheet:
            self.blit_m4_fire()
        elif self.awp_fire_sheet:
            self.blit_awp_fire()
        else:
            # if not firing any weapon, blit the normal image
            self.screen.blit(self.rotated_image, self.updated_rect)

        # draw health bar
        health_x = self.game_settings.screen_width - self.game_settings.health_bar_distancex
        health_y = self.game_settings.screen_height - self.game_settings.health_bar_distancey

        self.screen.blit(self.heart_image, (health_x - 30, health_y))  # draw heart
        pygame.draw.rect(self.screen, (0, 0, 0), (health_x, health_y, self.game_settings.max_health_bar_length, 20), 1)  # draw hp box
        pygame.draw.rect(self.screen, (255, 0, 0), (health_x + 1, health_y + 1, int(self.game_settings.max_health_bar_length * self.hp / self.game_settings.max_health_point) - 2, 18))

        # display ammo amount
        ammo_x = self.game_settings.weapon_distancex
        ammo_y = self.game_settings.screen_height - self.game_settings.weapon_distancey

        if self.current_weapon == self.game_settings.pistol:
            ammo_text_surface = gf.text_format(str(self.clip_pistol) + '/' + str(self.ammo_pistol), self.game_settings.digital_font_path, 40, self.game_settings.BRIGHT_YELLOW)
            self.screen.blit(ammo_text_surface, (ammo_x, ammo_y))
        if self.current_weapon == self.game_settings.m4:
            ammo_text_surface = gf.text_format(str(self.clip_m4) + '/' + str(self.ammo_m4), self.game_settings.digital_font_path, 40, self.game_settings.BRIGHT_YELLOW)
            self.screen.blit(ammo_text_surface, (ammo_x, ammo_y))
        if self.current_weapon == self.game_settings.awp:
            ammo_text_surface = gf.text_format(str(self.clip_awp) + '/' + str(self.ammo_awp), self.game_settings.digital_font_path, 40, self.game_settings.BRIGHT_YELLOW)
            self.screen.blit(ammo_text_surface, (ammo_x, ammo_y))

        # draw current weapon player carrying
        if self.current_weapon == self.game_settings.pistol:
            self.screen.blit(self.pistol_image, (ammo_x - 150, ammo_y - 40))
        if self.current_weapon == self.game_settings.m4:
            self.screen.blit(self.m4_image, (ammo_x - 150, ammo_y - 40))
        if self.current_weapon == self.game_settings.awp:
            self.screen.blit(self.awp_image, (ammo_x - 150, ammo_y - 40))

        # draw reload progress bar if player is reloading
        if self.reload_frame > 0:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.rect[0], self.rect[1] - 30, self.game_settings.max_reload_bar_length, 20), 1)
            pygame.draw.rect(self.screen, self.game_settings.BRIGHT_YELLOW, (self.rect[0] + 1, self.rect[1] - 29, int(self.game_settings.max_reload_bar_length * (1 - self.reload_frame / self.game_settings.reload_speed[self.current_weapon])) - 1, 18))
            reload_text = gf.text_format("Reloading...", self.game_settings.segoeui_path, 18, self.game_settings.BRIGHT_YELLOW)
            self.screen.blit(reload_text, (self.rect[0], self.rect[1] - 60))

    def blit_pistol_fire(self):
        rotated_image = pygame.transform.rotate(self.pistol_fire_sheet.pop(), 180 - self.angle)
        self.screen.blit(rotated_image, self.updated_rect)

    def blit_m4_fire(self):
        rotated_image = pygame.transform.rotate(self.m4_fire_sheet.pop(), 180 - self.angle)
        self.screen.blit(rotated_image, self.updated_rect)

    def blit_awp_fire(self):
        rotated_image = pygame.transform.rotate(self.awp_fire_sheet.pop(), 180 - self.angle)
        self.screen.blit(rotated_image, self.updated_rect)
