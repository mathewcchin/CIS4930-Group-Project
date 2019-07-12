import pygame
from setting import Settings  # for game settings
from player import PlayerPistol
import game_functions as gf


def run_game():
    """
    This function does following:
        -Initialize game objects
        -create a screen object
        -run the main game loop
        -deal with after-exiting tasks

    :return: Null
    """

    # # create a game setting object
    # game_settings = Settings()
    #
    # # initialize pygame and the main screen
    # pygame.init()
    # screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    # pygame.display.set_caption(game_settings.caption)

    # create objects that will displayed on game main screen
    background = pygame.image.load("img/bg.jpg")
    player = PlayerPistol(screen, game_settings)

    # start the main loop of the game
    while True:
        # check event
        gf.check_events(player)

        # update player stats
        player.update()

        # update screen
        gf.update_screen(background, player, screen)


# create a game setting object
game_settings = Settings()

# initialize pygame and the main screen
pygame.init()
screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
pygame.display.set_caption(game_settings.caption)

# run_game()
gf.welcome_screen(game_settings, screen)
