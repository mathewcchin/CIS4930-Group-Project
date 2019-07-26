import pygame
from pygame.sprite import Sprite
import random
import math
from setting import Settings


class PistolAmmo(Sprite):
    game_settings = Settings()

    def __init__(self, zombie):
        super().__init__()
        self.ammo_type = self.game_settings.pistol
        self.screen = zombie.screen
        self.image = pygame.image.load(self.game_settings.ammo_pistol_image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = zombie.rect.centerx + random.randint(-40, 40)
        self.rect.centery = zombie.rect.centery + random.randint(-40, 40)
        self.ammo_life = self.game_settings.pistol_ammo_life
        self.amount = random.randint(self.game_settings.pistol_ammo_min_amount, self.game_settings.pistol_ammo_max_amount)

    def blit_ammo(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.ammo_life -= 1


class M4Ammo(Sprite):
    game_settings = Settings()

    def __init__(self, zombie):
        super().__init__()
        self.ammo_type = self.game_settings.m4
        self.screen = zombie.screen
        self.image = pygame.image.load(self.game_settings.ammo_m4_image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = zombie.rect.centerx + random.randint(-40, 40)
        self.rect.centery = zombie.rect.centery + random.randint(-40, 40)
        self.ammo_life = self.game_settings.m4_ammo_life
        self.amount = random.randint(self.game_settings.m4_ammo_min_amount, self.game_settings.m4_ammo_max_amount)

    def blit_ammo(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.ammo_life -= 1


class AwpAmmo(Sprite):
    game_settings = Settings()

    def __init__(self, zombie):
        super().__init__()
        self.ammo_type = self.game_settings.awp
        self.screen = zombie.screen
        self.image = pygame.image.load(self.game_settings.ammo_awp_image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = zombie.rect.centerx + random.randint(-40, 40)
        self.rect.centery = zombie.rect.centery + random.randint(-40, 40)
        self.ammo_life = self.game_settings.awp_ammo_life
        self.amount = random.randint(self.game_settings.awp_ammo_min_amount, self.game_settings.awp_ammo_max_amount)

    def blit_ammo(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.ammo_life -= 1