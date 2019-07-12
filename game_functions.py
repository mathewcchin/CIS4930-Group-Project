import sys
import pygame
import math  # for rotation angle calculation
import random
from pygame.sprite import Group  # for grouping multiple objects based on pygame.sprite
from bullet_pistol import BulletPistol
from setting import Settings
from player import PlayerPistol


def run_game(screen, game_settings):
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

    # create Group() object to store bullets that was shot
    bullets_pistol = Group()

    # start the main loop of the game
    while True:
        # check event
        check_events(player, bullets_pistol, game_settings, screen)

        # update player stats
        player.update()

        # update bullets
        bullets_pistol.update()

        # update screen
        update_screen(background, player, screen, bullets_pistol)


def blit_player(player, screen):
    """
    This function deals with the rotation of the player's character along with mouse

    Ideas:
        To display the player onto the screen, we have to call screen.blit(image, rect). The image is the "surface" of the player, while the rect is the rectangle of the player. Rotation will only affect the rotated angle of player's image surface. To achieve this, we first get the position of mouse pointer using:
            pygame.mouse.get_pos()
        This will return a tuple, which is (x, y), containing x and y value of mouse's position. Then we can get the coordinate of player.rect's center:
            (player.rect.centerx, player.rect.centery)
        We have two points, which is the mouse pointer and the center of player's character's center. We can obtain the rotation angle:
            angle = math.atan2(player.rect.centery - mouse_position[1], player.rect.centerx - mouse_position[0]) * 57.29

        Pay attention the angle returned by math.atan2() is in rad, we have to convert it to degrees.

        Then we rotate player's image to reflect this change. One important thing is, we shouldn't modify the original image (stored in player's object). Here, we use another variable to hold the rotated player's image:
            player_rotated_image = pygame.transform.rotate(player.image, 180 - angle)

        Then, we blit this rotated image to the screen, rather than the original image. This is because we have to keep the original image so we can use it as a reference to calculate the rotated angle.

        Before we blit, we have to get the new rect. When the image is rotated, "the image will be padded larger to hold the new size", which means a larger rect is created that surrounds the image.

    Parameters:
        player:
    """

    # get mouse coordinate
    mouse_position = pygame.mouse.get_pos()
    # calculate angle, 1 rad = 57.29 degrees
    angle = math.atan2(player.rect.centery - mouse_position[1], player.rect.centerx - mouse_position[0]) * 57.29
    # rotate player's image surface and store rotated image in player's object
    player.rotated_image = pygame.transform.rotate(player.image, 180 - angle)

    # find out where to blit the rotated image (coordinate of the upper left corner), store the updated rect in player's object
    player.updated_rect = (player.rect.centerx - player.rotated_image.get_rect().width / 2,
                           player.rect.centery - player.rotated_image.get_rect().height / 2)

    # blit the new position
    screen.blit(player.rotated_image, player.updated_rect)


def check_keydown_events(event, player):
    """
    This function will check which key is pressed down, and then perform corresponding operations.
    """

    if event.key == pygame.K_w:
        player.moving_up = True

    if event.key == pygame.K_a:
        player.moving_left = True

    if event.key == pygame.K_s:
        player.moving_down = True

    if event.key == pygame.K_d:
        player.moving_right = True


def check_keyup_events(event, player):
    if event.key == pygame.K_w:
        player.moving_up = False

    if event.key == pygame.K_a:
        player.moving_left = False

    if event.key == pygame.K_s:
        player.moving_down = False

    if event.key == pygame.K_d:
        player.moving_right = False


def check_mousedown(event, player, bullets, game_settings, screen):
    """
    Parameter:
        player: used to calculate the position and angle of the bullet
        bullets: will add bullet to this group, if left mouse clicked
    """

    # left click
    if event.button == 1 and len(bullets.sprites()) < 1:
        # play the shooting sound at channel 1
        pistol_sound = pygame.mixer.Sound('sfx/weapons/p228.wav')
        pisto_channel = pygame.mixer.Channel(1)
        pisto_channel.play(pistol_sound)

        # create a pistol bullet and add to bullets
        new_bullet = BulletPistol(game_settings, screen, player)
        bullets.add(new_bullet)


def check_events(player, bullets, game_settings, screen):
    """
    Check the broad category and call corresponding methods to do the specific work
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, player)

        if event.type == pygame.KEYUP:
            check_keyup_events(event, player)

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mousedown(event, player, bullets, game_settings, screen)


def update_screen(background, player, screen, bullets):
    """
    Redraw screens (after items on the screen are updated)
    """
    # draw background
    screen.blit(background, (0, 0))

    # update and draw player's character
    blit_player(player, screen)

    # blit each bullet, delete it if out of screen (using a copy)
    for bullet in bullets.copy().sprites():
        if bullet.rect.bottom < 0 or bullet.rect.top > screen.get_height() or bullet.rect.left > screen.get_width() or bullet.rect.right < 0:  # out of screen
            bullets.remove(bullet)
        else:
            bullet.blit_bullet()

    # draw the updated screen
    pygame.display.flip()


def welcome_screen(game_settings, screen):
    # Game sounds:
    # Main Menu (Royalty Free Soundtrack):
    # Power Bots Loop
    # by DL-Sounds
    # https://www.dl-sounds.com/royalty-free/power-bots-loop/

    pygame.mixer.music.load("img/Power Bots Loop.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    # key click noise:
    # Menu_Navigate_03.wav
    # by LittleRobotSoundFactory
    # https://freesound.org/people/LittleRobotSoundFactory/sounds/270315/
    key_sound = pygame.mixer.Sound("img/key_sound.wav")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (192, 192, 192)

    # Game Fonts
    font = game_settings.font

    # Game FPS
    clock = pygame.time.Clock()
    FPS = 30

    # Main Menu Loop
    selected = "start"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if selected == "settings" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "start"

                elif selected == "quit" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "settings"

                elif selected == "start" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "settings"

                elif selected == "settings" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "quit"

                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        run_game(screen, game_settings)
                    if selected == "settings":
                        user_settings()
                    if selected == "quit":
                        sys.exit()

        # Main Menu UI
        menu = pygame.image.load('img/bg.jpg')
        screen.blit(menu, (0, 0))

        title = text_format("Alien Invasion", font, 90, black)
        if selected == "start":
            text_start = text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)

        if selected == "settings":
            text_settings = text_format("SETTINGS", font, 75, white)
        else:
            text_settings = text_format("SETTINGS", font, 75, black)

        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        settings_rect = text_settings.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (game_settings.screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (game_settings.screen_width / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 350))
        screen.blit(text_quit, (game_settings.screen_width / 2 - (quit_rect[2] / 2), 400))
        pygame.display.update()
        clock.tick(FPS)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def user_settings():
    print("its working")
    # pygame.draw.rect(screen, (200, 150, 100, 50))

