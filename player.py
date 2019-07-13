import pygame
import random  # for playing foot steps randomly
import math  # for calculating rotated angle 


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
        self.fire_image = pygame.image.load('img/player_pistol_fire.jpg')
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

    def update(self):
        """
        This method will do following:
            1. update the coordinate of player's rect 
            2. play foot step if player is moving
            3. update the rotation of player's image
            
        """
        # play random foot step sound while moving flag is true
        # if the character is near the boundary, don't play sound
        if (self.moving_down and self.rect.bottom + self.game_settings.allowed_margin < self.screen_rect.bottom) or (
                self.moving_left and self.rect.left > self.game_settings.allowed_margin) or (
                self.moving_right and self.rect.right + self.game_settings.allowed_margin < self.screen_rect.right) or (
                self.moving_up and self.rect.top > self.game_settings.allowed_margin):
            if not self.foot_steps_channel.get_busy():  # if foot step channel is not playing
                self.foot_steps_channel.play(self.foot_steps[random.randint(0, 3)])

        # stop playing sound effect when player stopped
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.foot_steps_channel.stop()

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
        # 1 rad = 57.29 degrees
        self.angle = math.atan2(self.rect.centery - mouse_position[1], self.rect.centerx - mouse_position[0]) * 57.29
        
        # rotate player's image surface and store rotated image in player's object
        self.rotated_image = pygame.transform.rotate(self.image, 180 - self.angle)

        # find out where to blit the rotated image (coordinate of the upper left corner), store the updated rect in player's object
        self.updated_rect = (self.rect.centerx - self.rotated_image.get_rect().width / 2,
                               self.rect.centery - self.rotated_image.get_rect().height / 2)
        

    
    def display_firing(self):
        # rotate the fire image according to current mouse position
        self.rotated_fire_image = pygame.transform.rotate(self.fire_image, 180 - self.angle)
        # blit and show the fire frame
        for i in range(30):
          self.screen.blit(self.rotated_fire_image, self.updated_rect)
          pygame.display.flip()