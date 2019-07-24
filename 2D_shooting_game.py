import pygame
from setting import Settings  # for game settings
import game_functions as gf
from player import PlayerPistol

# create a game setting object
game_settings = Settings()

# initialize pygame and the main screen
pygame.init()
screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
pygame.display.set_caption(game_settings.caption)
player = PlayerPistol(screen, game_settings)

# run welcome screen
gf.welcome_screen(screen, game_settings, player)
#gf.run_game(screen, game_settings, player)
