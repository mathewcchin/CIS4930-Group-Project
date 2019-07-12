import pygame
from pygame.sprite import Sprite


class BulletPistol(Sprite):
    """
    A class to manage bullets fired by player_pistol.

    Using similar idea in the alien invasion example
    """

    def __init__(self, game_settings, screen, player, mouse_position):
        """
        Create a bullet object at the player's pistol position
        (need player's position and mouse rotation info to determine final position)

        Parameters:
            game_settings: an object of Settings class, will use bullet setting inside

            screen: screen onto which the bullet will be drawn

            player: the player's character object, used to determine the position of the bullet

            mouse_position: current mouse position, used to determine the position of the bullet
        """

        super().__init__()
        self.screen = screen  # used to draw Bullet on main screen
