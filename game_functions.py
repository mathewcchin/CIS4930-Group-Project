import sys
import pygame
import math  # for rotation angle calculation
import random
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

    # create objects that will displayed on game main screen
    background = pygame.image.load("img/bg.jpg")
    player = PlayerPistol(screen, game_settings)

    # start the main loop of the game
    while True:
        # check event
        check_events(player)

        # update player stats
        player.update()

        # update screen
        update_screen(background, player, screen)


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
    # rotate player's image surface
    player_rotated_image = pygame.transform.rotate(player.image, 180 - angle)

    # find out where to blit the rotated image (coordinate of the upper left corner)
    player_updated_rect = (player.rect.centerx - player_rotated_image.get_rect().width / 2,
                           player.rect.centery - player_rotated_image.get_rect().height / 2)

    # blit the new position
    screen.blit(player_rotated_image, player_updated_rect)


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


def check_mousedown(event):
    # left click
    if event.button == 1:
        s = pygame.mixer.Sound('sfx/weapons/p228.wav')
        pisto_channel = pygame.mixer.Channel(1)
        pisto_channel.play(s)


def check_events(player):
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
            check_mousedown(event)


def update_screen(background, player, screen):
    """
    Redraw screens (after items on the screen are updated)
    """

    # plot background
    screen.blit(background, (0, 0))

    # update and draw player's character
    blit_player(player, screen)

    # draw the updated screen
    pygame.display.flip()


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def user_settings(screen, game_settings):
    print("user settings:")

    # screen.fill(game_settings.color_black)

    # creating player instruction
    instructions = text_format("Instructions", game_settings.font, 75, game_settings.color_black)
    movement_instructions = text_format("Movement . . . .", game_settings.font, 70, game_settings.color_black)
    move_up = text_format("up. . . . . w key", game_settings, 60, game_settings.color_black)
    move_down = text_format("down. . . . . s key", game_settings, 60, game_settings.color_black)
    move_left = text_format("left. . . . . a key", game_settings, 60, game_settings.color_black)
    move_right = text_format("right. . . . . d key", game_settings, 60, game_settings.color_black)
    shooting_instructions = text_format("shoot . . . . spacebar", game_settings, 70, game_settings.color_black)

    #
    instruction_rect = instructions.get_rect()
    movement_instructions_rect = movement_instructions.get_rect()
    move_up_rect = move_up.get_rect()
    move_down_rect = move_down.get_rect()
    move_left_rect = move_left.get_rect()
    move_right_rect = move_right.get_rect()
    shooting_instructions_rect = shooting_instructions.get_rect()

    # adding instructions to the screen
    screen.blit(instructions, (game_settings.screen_width / 2 - (instruction_rect[2] / 2), 80))
    screen.blit(movement_instructions, (game_settings.screen_width / 2 - (movement_instructions_rect[2] / 2), 100))
    screen.blit(move_up, (game_settings.screen_width / 2 - (move_up_rect[2] / 2), 80))
    screen.blit(move_down, (game_settings.screen_width / 2 - (move_down_rect[2] / 2), 80))
    screen.blit(move_left, (game_settings.screen_width / 2 - (move_left_rect[2] / 2), 80))
    screen.blit(move_right, (game_settings.screen_width / 2 - (move_right_rect[2] / 2), 80))
    screen.blit(shooting_instructions, (game_settings.screen_width / 2 - (shooting_instructions_rect[2] / 2), 80))

    # draw the updated screen
    pygame.display.update()

def welcome_screen(game_settings, screen):
    # Game sounds:
    # Main Menu (Royalty Free Soundtrack):
    # Power Bots Loop
    # by DL-Sounds
    # https://www.dl-sounds.com/royalty-free/power-bots-loop/

    pygame.mixer.music.load("img/Power Bots Loop.wav")
    pygame.mixer.music.play(-1)

    # key click noise:
    # Menu_Navigate_03.wav
    # by LittleRobotSoundFactory
    # https://freesound.org/people/LittleRobotSoundFactory/sounds/270315/
    key_sound = pygame.mixer.Sound("img/key_sound.wav")

    # Game Fonts
    font = game_settings.font

    # Game FPS
    clock =
    FPS = 30

    # Main Menu Loop
    selected = "new game"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if selected == "new game" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "quit"

                elif selected == "load game" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "new game"

                elif selected == "settings" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "load game"

                elif selected == "quit" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "settings"

                elif selected == "new game" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "load game"

                elif selected == "load game" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "settings"

                elif selected == "settings" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "quit"

                elif selected == "quit" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "new game"

                if event.key == pygame.K_RETURN:
                    if selected == "new game":
                        run_game(screen, game_settings)
                    if selected == "load game":
                        print("loading game")
                    if selected == "settings":
                        user_settings(screen, game_settings)
                    if selected == "quit":
                        sys.exit()

        # Main Menu UI
        menu = pygame.image.load('img/bg.jpg')
        screen.blit(menu, (0, 0))

        title = text_format("Alien Invasion", font, 90, game_settings.color_black)
        if selected == "new game":
            text_new_game = text_format("NEW GAME", font, 75, game_settings.color_white)
        else:
            text_new_game = text_format("NEW GAME", font, 75, game_settings.color_black)

        if selected == "load game":
            text_load_game = text_format("LOAD GAME", font, 75, game_settings.color_white)
        else:
            text_load_game = text_format("LOAD GAME", font, 75, game_settings.color_black)

        if selected == "settings":
            text_settings = text_format("SETTINGS", font, 75, game_settings.color_white)
        else:
            text_settings = text_format("SETTINGS", font, 75, game_settings.color_black)

        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, game_settings.color_white)
        else:
            text_quit = text_format("QUIT", font, 75, game_settings.color_black)

        title_rect = title.get_rect()
        new_game_rect = text_new_game.get_rect()
        load_game_rect = text_load_game.get_rect()
        settings_rect = text_settings.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (game_settings.screen_width / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_new_game, (game_settings.screen_width / 2 - (new_game_rect[2] / 2), 300))
        screen.blit(text_load_game, (game_settings.screen_width / 2 - (load_game_rect[2] / 2), 350))
        screen.blit(text_settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 400))
        screen.blit(text_quit, (game_settings.screen_width / 2 - (quit_rect[2] / 2), 450))
        pygame.display.update()
        clock.tick(FPS)

