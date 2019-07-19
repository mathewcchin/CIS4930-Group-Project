import sys
import pygame
import math  # for rotation angle calculation
import random
from pygame.sprite import Group  # for grouping multiple objects based on pygame.sprite
from bullet_pistol import BulletPistol
from setting import Settings
from player import PlayerPistol
from zombie import Zombie


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

    # create Group() object to store bullets that was shot
    bullets_pistol = Group()

    # create another Group() object to store zombies
    zombies = Group()
    last_spawn_time = pygame.time.get_ticks()  # record zombie spawn time

    # start the main loop of the game
    while True:
        # check event
        check_events(player, bullets_pistol, game_settings, screen)

        # generate zombies
        last_spawn_time = spawn_zombies(zombies, player, game_settings, screen, last_spawn_time)
        
        # delete zombies and bullets when zombie is shot by bullet
        shoot_zombie(zombies, bullets_pistol)
        
        # update player stats (rotation and position)
        player.update()
        
        # update zombie
        zombies.update()

        # update bullets
        bullets_pistol.update()

        # update screen
        update_screen(background, player, zombies, screen, bullets_pistol)


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


def is_mouse_in_player(player):
    """
    Check if the mouse is very close to player
    """
    mouse_position = pygame.mouse.get_pos()

    if mouse_position[0] >= player.updated_rect.left and mouse_position[0] <= player.updated_rect.right and mouse_position[1] >= player.updated_rect.top and mouse_position[1] <= player.updated_rect.bottom:
        return True

    return False


def check_mousedown(event, player, bullets, game_settings, screen):
    """
    Parameter:
        player: used to calculate the position and angle of the bullet
        bullets: will add bullet to this group, if left mouse clicked
    """

    # left click
    if event.button == 1 and pygame.time.get_ticks() - player.last_shooting_time >= game_settings.pistol_shooting_interval and not is_mouse_in_player(player):
        # play the shooting sound at channel 1
        pistol_sound = pygame.mixer.Sound('sfx/weapons/p228.wav')
        pisto_channel = pygame.mixer.Channel(1)
        pisto_channel.play(pistol_sound)

        # create a pistol bullet and add to bullets
        new_bullet = BulletPistol(game_settings, screen, player)
        bullets.add(new_bullet)

        # show fire frame
        player.display_firing()

        # update player's last shooting time
        player.last_shooting_time = pygame.time.get_ticks()


def check_events(player, bullets, game_settings, screen):
    """
    Check the broad category and call corresponding methods to do the specific work
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, player)

            # Implementation of a pause function:
            if event.key == pygame.K_ESCAPE:
                pause_game(screen, game_settings)

        if event.type == pygame.KEYUP:
            check_keyup_events(event, player)

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mousedown(event, player, bullets, game_settings, screen)


def spawn_zombies(zombies, player, game_settings, screen,  last_spawn_time):
    # if time interval is less than spawn time, do nothing
    if pygame.time.get_ticks() - last_spawn_time < game_settings.spawn_time:
        return last_spawn_time

    # if time interval is larger than spawn time, create a new zombie in zombies
    new_zombie = Zombie(game_settings, screen, player)
    zombies.add(new_zombie)

    # return new spawn time
    return pygame.time.get_ticks()


def shoot_zombie(zombies, bullets):
    for zombie in zombies.copy().sprites():
        for bullet in bullets.copy().sprites():
            if zombie.rect.colliderect(bullet.rect):
                bullets.remove(bullet)
                zombies.remove(zombie)


def update_screen(background, player, zombies, screen, bullets):
    """
    Redraw screens (after items on the screen are updated)
    """
    # draw background
    screen.blit(background, (0, 0))

    # draw player's character to screen
    screen.blit(player.rotated_image, player.updated_rect)

    # draw each zombie to screen
    for zombie in zombies:
        zombie.blit_zombie()

    # blit each bullet, delete it if it is out of screen
    for bullet in bullets.copy().sprites():
        if bullet.rect.bottom < 0 or bullet.rect.top > screen.get_height() or bullet.rect.left > screen.get_width() or bullet.rect.right < 0:  # out of screen
            bullets.remove(bullet)
        else:
            bullet.blit_bullet()

    # draw the updated screen on the game window
    pygame.display.flip()


def welcome_screen(screen, game_settings):
    # Game sounds:
    # Main Menu (Royalty Free Soundtrack):
    # Power Bots Loop
    # by DL-Sounds
    # https://www.dl-sounds.com/royalty-free/power-bots-loop/

    pygame.mixer.music.load("sfx/power_bots_loop.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    # key click noise:
    # Menu_Navigate_03.wav
    # by LittleRobotSoundFactory
    # https://freesound.org/people/LittleRobotSoundFactory/sounds/270315/
    key_sound = pygame.mixer.Sound("sfx/key_sound.wav")

    # Game Fonts
    font = game_settings.font

    # Game FPS
    clock = pygame.time.Clock()
    FPS = game_settings.FPS

    # Main Menu Loop to display menus
    selected = "new game"  # store current selected option
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

        title = text_format(game_settings.caption, font, 100, game_settings.color_black)
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
        screen.blit(title, (game_settings.screen_width / 2 - (title_rect[2] / 2), 150))
        screen.blit(text_new_game, (game_settings.screen_width / 2 - (new_game_rect[2] / 2), 300))
        screen.blit(text_load_game, (game_settings.screen_width / 2 - (load_game_rect[2] / 2), 350))
        screen.blit(text_settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 400))
        screen.blit(text_quit, (game_settings.screen_width / 2 - (quit_rect[2] / 2), 450))
        pygame.display.update()
        clock.tick(FPS)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def user_settings(screen, game_settings):
    # create objects that will displayed on game main screen
    background = pygame.image.load("img/bg.jpg")

    while True:
        screen.blit(background, (0, 0))

        # creating player instruction
        instructions = text_format("Instructions", game_settings.font, 75, game_settings.color_black)
        movement_instructions = text_format("Movement . . .", game_settings.font, 60, game_settings.color_black)
        move_up = text_format("move up . . . . . . . . . . w key", game_settings.font, 50, game_settings.color_black)
        move_down = text_format("move down . . . . . . . . s key", game_settings.font, 50, game_settings.color_black)
        move_left = text_format("move left . . . . . . . . . a key", game_settings.font, 50, game_settings.color_black)
        move_right = text_format("move right . . . . . . . . d key", game_settings.font, 50, game_settings.color_black)

        shooting_instructions = text_format("Shooting and aim . . .", game_settings.font, 60, game_settings.color_black)
        shoot = text_format("shoot . . . . . . . . . . left click", game_settings.font, 50, game_settings.color_black)
        aim = text_format("aim . . . . . . . mouse rotation", game_settings.font, 50, game_settings.color_black)

        exit_screen = text_format("Press esc to return to main menu", game_settings.font, 60, game_settings.color_black)

        instruction_rect = instructions.get_rect()
        movement_instructions_rect = movement_instructions.get_rect()
        move_up_rect = move_up.get_rect()
        move_down_rect = move_down.get_rect()
        move_left_rect = move_left.get_rect()
        move_right_rect = move_right.get_rect()

        shooting_instructions_rect = shooting_instructions.get_rect()
        shoot_rect = shoot.get_rect()
        aim_rect = aim.get_rect()

        exit_screen_rect = exit_screen.get_rect()

        # adding instructions to the screen
        screen.blit(instructions, (game_settings.screen_width / 2 - (instruction_rect[2] / 2), 80))
        screen.blit(movement_instructions, (game_settings.screen_width / 2 - (movement_instructions_rect[2]), 160))
        screen.blit(move_up, (game_settings.screen_width / 2 - (move_up_rect[2] / 2), 220))
        screen.blit(move_down, (game_settings.screen_width / 2 - (move_down_rect[2] / 2), 260))
        screen.blit(move_left, (game_settings.screen_width / 2 - (move_left_rect[2] / 2), 300))
        screen.blit(move_right, (game_settings.screen_width / 2 - (move_right_rect[2] / 2), 340))

        screen.blit(shooting_instructions, (game_settings.screen_width / 3 - (shooting_instructions_rect[2] / 3), 400))
        screen.blit(shoot, (game_settings.screen_width / 2 - (shoot_rect[2] / 2), 460))
        screen.blit(aim, (game_settings.screen_width / 2 - (aim_rect[2] / 2), 500))

        screen.blit(exit_screen, (game_settings.screen_width / 2 - (exit_screen_rect[2] / 2), 600))

        # checking for player input to quit instruction screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.key == pygame.K_ESCAPE:
                return

        # draw the updated screen
        pygame.display.flip()

# creating player instruction
def pause_game(screen, game_settings):

    pause = text_format("Pause Game", game_settings.font, 100, game_settings.color_black)
    pause_rect = pause.get_rect()
    screen.blit(pause, (game_settings.screen_width / 2 - (pause_rect[2] / 2), 150))

    key_sound = pygame.mixer.Sound('sfx/key_sound.wav')
    clock = pygame.time.Clock()

    selected = "Save Game"
    while True:
        # checking for player input to quit instruction screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                elif event.key == pygame.K_DOWN and selected == "Save Game":
                    key_sound.play()
                    selected = "Game Settings"

                elif event.key == pygame.K_DOWN and selected == "Game Settings":
                    key_sound.play()
                    selected = "Return to Main Menu"

                elif event.key == pygame.K_DOWN and selected == "Return to Main Menu":
                    key_sound.play()
                    selected = "Exit Game"

                elif event.key == pygame.K_DOWN and selected == "Exit Game":
                    key_sound.play()
                    selected = "Save Game"

                elif event.key == pygame.K_UP and selected == "Game Settings":
                    key_sound.play()
                    selected = "Save Game"

                elif event.key == pygame.K_UP and selected == "Return to Main Menu":
                    key_sound.play()
                    selected = "Game Settings"

                elif event.key == pygame.K_UP and selected == "Exit Game":
                    key_sound.play()
                    selected = "Return to Main Menu"

                elif event.key == pygame.K_UP and selected == "Save Game":
                    key_sound.play()
                    selected = "Exit Game"

                if event.key == pygame.K_RETURN:
                    if selected == "Save Game":
                        print("Save Game")
                    elif selected == "Game Settings":
                        user_settings(screen, game_settings)
                    elif selected == "Return to Main Menu":
                        welcome_screen(screen, game_settings)
                    elif selected == "Exit Game":
                        sys.exit()

        # creating Pause Game instruction
        if selected == "Save Game":
            save_game = text_format("Save Game", game_settings.font, 60, game_settings.color_white)
        else:
            save_game = text_format("Save Game", game_settings.font, 60, game_settings.color_black)

        if selected == "Game Settings":
            settings = text_format("Game Settings", game_settings.font, 60, game_settings.color_white)
        else:
            settings = text_format("Game Settings", game_settings.font, 60, game_settings.color_black)

        if selected == "Return to Main Menu":
            main_menu = text_format("Return to Main Menu", game_settings.font, 60, game_settings.color_white)
        else:
            main_menu = text_format("Return to Main Menu", game_settings.font, 60, game_settings.color_black)

        if selected == "Exit Game":
            exit_game = text_format("Exit Game", game_settings.font, 60, game_settings.color_white)
        else:
            exit_game = text_format("Exit Game", game_settings.font, 60, game_settings.color_black)

        save_game_rect = save_game.get_rect()
        settings_rect = settings.get_rect()
        main_menu_rect = main_menu.get_rect()
        exit_game_rect = exit_game.get_rect()

        # drawing player pause-menu text to the screen
        screen.blit(save_game, (game_settings.screen_width / 2 - (save_game_rect[2] / 2), 300))
        screen.blit(settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 340))
        screen.blit(main_menu, (game_settings.screen_width / 2 - (main_menu_rect[2] / 2), 380))
        screen.blit(exit_game, (game_settings.screen_width / 2 - (exit_game_rect[2] / 2), 420))

        # draw the updated screen
        pygame.display.flip()

        clock.tick(game_settings.FPS)
