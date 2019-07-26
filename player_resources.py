import pygame


pygame.mixer.pre_init(44100, -16, 1, 2048)
pygame.init()


class PlayerResources:
    """hold pre-loaded animations"""
    def __init__(self, game_settings):
        self.game_settings = game_settings

        self.pistol_fire_sheet = []
        self.m4_fire_sheet = []
        self.awp_fire_sheet = []

        self.pistol_fire_paths = game_settings.pistol_fire_frame_paths
        self.m4_fire_paths = game_settings.m4_fire_frame_paths
        self.awp_fire_paths = game_settings.awp_fire_frame_paths

        # load fire frame
        for i in range(len(self.pistol_fire_paths)):
            for j in range(game_settings.pistol_fire_frame_multiplier):
                self.pistol_fire_sheet.append(pygame.image.load(self.pistol_fire_paths[i]))

        for i in range(len(self.m4_fire_paths)):
            for j in range(game_settings.m4_fire_frame_multiplier):
                self.m4_fire_sheet.append(pygame.image.load(self.m4_fire_paths[i]))

        for i in range(len(self.awp_fire_paths)):
            for j in range(game_settings.awp_fire_frame_multiplier):
                self.awp_fire_sheet.append(pygame.image.load(self.awp_fire_paths[i]))

