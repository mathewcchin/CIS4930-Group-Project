import pygame
import random


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
        This is to update the coordinate of the character image (not rotation, rotation is done by game_functions.blit_player())

        This function will check the moving flag of the player object and perform moving.
        It will also play foot step sound effects while moving.
        """
        # play random foot step sound while moving flag is true
        # if the character is near the boundary, don't play sound
        if (self.moving_down and self.rect.bottom + 20 < self.screen_rect.bottom) or (
                self.moving_left and self.rect.left > 20) or (
                self.moving_right and self.rect.right + 20 < self.screen_rect.right) or (
                self.moving_up and self.rect.top > 20):
            if not self.foot_steps_channel.get_busy():  # if foot step channel is not playing
                self.foot_steps_channel.play(self.foot_steps[random.randint(0, 3)])
                # self.foot_steps[random.randint(0, 3)].play(0)
        # stop playing sound effect when player stopped
        if not self.moving_down and not self.moving_left and not self.moving_right and not self.moving_up:
            self.foot_steps_channel.stop()

        # move player
        if self.moving_down and self.rect.bottom + 20 < self.screen_rect.bottom:
            self.rect.centery += self.game_settings.character_speed

        if self.moving_left and self.rect.left > 20:
            self.rect.centerx -= self.game_settings.character_speed

        if self.moving_right and self.rect.right + 20 < self.screen_rect.right:
            self.rect.centerx += self.game_settings.character_speed

        if self.moving_up and self.rect.top > 20:
            self.rect.centery -= self.game_settings.character_speed
