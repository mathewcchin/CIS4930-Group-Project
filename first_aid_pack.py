import pygame
from pygame.sprite import Sprite
import random
import math
from setting import Settings


class FirstAidPack(Sprite):
    game_settings = Settings()

    def __init__(self, zombie):
        super().__init__()
        self.screen = zombie.screen
        self.image = pygame.image.load(self.game_settings.first_aid_pack_image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = zombie.rect.centerx + random.randint(-50, 50)
        self.rect.centery = zombie.rect.centery + random.randint(-50, 50)
        self.pack_life = self.game_settings.first_aid_pack_life
        self.heal_amount = random.randint(self.game_settings.first_aid_min_amount, self.game_settings.first_aid_min_amount)

    def blit_pack(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.pack_life -= 1
