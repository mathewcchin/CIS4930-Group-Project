import sys
import pygame
import math  # for rotation angle calculation
import random
from pygame.sprite import Group  # for grouping multiple objects based on pygame.sprite
from bullet_pistol import BulletPistol
from setting import Settings
from player import PlayerPistol
from zombie import *
from userinfo import User
from user_registration import *


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
    background = pygame.image.load("img/bg.jpg").convert_alpha()
    player = PlayerPistol(screen, game_settings)

    # create Group() object to store bullets that was shot
    bullets_pistol = Group()

    # create another Group() object to store zombies
    zombies = Group()
    last_spawn_time = pygame.time.get_ticks()  # record zombie spawn time

    # create a Group() object to store dead zombies
    dead_zombies = Group()

    # controls game fps
    clock = pygame.time.Clock()

    # start the main loop of the game
    while True:
        # FPS
        clock.tick(game_settings.FPS)

        # check event
        check_events(player, bullets_pistol, game_settings, screen)

        # generate zombies
        last_spawn_time = spawn_zombies(zombies, player, game_settings, screen, last_spawn_time)

        # delete zombies and bullets when zombie is shot by bullet
        shoot_zombie(zombies, bullets_pistol, dead_zombies)

        # update player stats (rotation and position)
        player.update()

        # update zombie
        zombies.update()

        # update dead_zombie
        dead_zombies.update()

        # update bullets
        bullets_pistol.update()

        # update screen
        update_screen(background, player, zombies, screen, bullets_pistol, dead_zombies)


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

    if mouse_position[0] >= player.updated_rect.left and mouse_position[0] <= player.updated_rect.right and \
            mouse_position[1] >= player.updated_rect.top and mouse_position[1] <= player.updated_rect.bottom:
        return True

    return False


def check_mousedown(event, player, bullets, game_settings, screen):
    """
    Parameter:
        player: used to calculate the position and angle of the bullet
        bullets: will add bullet to this group, if left mouse clicked
    """

    # left click
    if event.button == 1 and pygame.time.get_ticks() - player.last_shooting_time >= game_settings.pistol_shooting_interval and not is_mouse_in_player(
            player):
        # play the shooting sound at channel 1
        pistol_sound = pygame.mixer.Sound('sfx/weapons/usp.wav')
        pisto_channel = pygame.mixer.Channel(game_settings.pistol_channel)
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
        if event.type == pygame.K_ESCAPE:
            pause_game(screen, game_settings)

        if event.type == pygame.KEYUP:
            check_keyup_events(event, player)

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mousedown(event, player, bullets, game_settings, screen)


def spawn_zombies(zombies, player, game_settings, screen, last_spawn_time):
    # if time interval is less than spawn time, do nothing
    if pygame.time.get_ticks() - last_spawn_time < game_settings.spawn_time:
        return last_spawn_time

    # if time interval is larger than spawn time, create a new zombie in zombies
    new_zombie = Zombie(game_settings, screen, player)
    zombies.add(new_zombie)

    # return new spawn time
    return pygame.time.get_ticks()


def shoot_zombie(zombies, bullets, dead_zombies):
    for zombie in zombies.copy().sprites():
        for bullet in bullets.copy().sprites():
            if zombie.rect.colliderect(bullet.rect):
                # play the hitting sound effect
                hit_sound = pygame.mixer.Sound('sfx/zombie/hit3.wav')
                hit_channel = pygame.mixer.Channel(zombie.game_settings.zombie_hit_channel)
                hit_channel.play(hit_sound)

                # remove bullets and zombies
                bullets.remove(bullet)
                zombies.remove(zombie)

                # create a new dead zombie and add to dead_zombies
                new_dead_zombie = DeadZombie(zombie.angle, zombie.updated_rect, zombie.game_settings, zombie.screen)
                dead_zombies.add(new_dead_zombie)


def update_screen(background, player, zombies, screen, bullets, dead_zombies):
    """
    Redraw screens (after items on the screen are updated)
    """
    # draw background
    screen.blit(background, (0, 0))

    # blit each bullet, delete it if it is out of screen
    for bullet in bullets.copy().sprites():
        if bullet.rect.bottom < 0 or bullet.rect.top > screen.get_height() or bullet.rect.left > screen.get_width() or bullet.rect.right < 0:  # out of screen
            bullets.remove(bullet)
        else:
            bullet.blit_bullet()

    # blit each dead zombie's death animation, delete it if all frames are displayed
    for dead_zombie in dead_zombies.copy().sprites():
        if not dead_zombie.death_images:  # remove zombie that finished displaying death frames
            dead_zombies.remove(dead_zombie)
        else:
            dead_zombie.blit_death_frame()

    # draw player's character to screen
    screen.blit(player.rotated_image, player.updated_rect)

    # draw each zombie to screen
    for zombie in zombies:
        zombie.blit_zombie()

    # draw the updated screen on the game window
    pygame.display.flip()


def welcome_screen(screen, game_settings):
    # Game sounds:
    # Main Menu (Royalty Free Soundtrack):
    # Power Bots Loop
    # by DL-Sounds
    # https://www.dl-sounds.com/royalty-free/power-bots-loop/

    pygame.mixer.music.load("sfx/power_bots_loop.wav")
    # pygame.mixer.music.play(-1)
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
                        create_user(screen, game_settings)
                        run_game(screen, game_settings)
                    if selected == "load game":
                        list = ["mathew", "bob", "kennan", "jessica"]
                        load_user(screen, game_settings, list)
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
        instructions = text_format("Game Instructions", game_settings.font, 75, game_settings.color_black)
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


def pause_game(screen, game_settings):
    # draws background
    background = pygame.image.load("img/bg.jpg")

    # in-game fx sound for whenever the user presses the up or down arrow key
    key_sound = pygame.mixer.Sound('sfx/key_sound.wav')
    clock = pygame.time.Clock()

    # Pause Game selection menu
    selected = "Save Game"
    while True:
        screen.blit(background, (0, 0))

        # checking for player input to quit instruction screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_DOWN and selected == "Save Game":
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
                        saved_user(screen, game_settings)
                    elif selected == "Game Settings":
                        user_settings(screen, game_settings)
                    elif selected == "Return to Main Menu":
                        welcome_screen(screen, game_settings)
                    elif selected == "Exit Game":
                        sys.exit()

        # creating Pause Game instruction
        pause = text_format("Pause Game", game_settings.font, 100, game_settings.color_black)

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

        pause_rect = pause.get_rect()
        save_game_rect = save_game.get_rect()
        settings_rect = settings.get_rect()
        main_menu_rect = main_menu.get_rect()
        exit_game_rect = exit_game.get_rect()

        # drawing player pause-menu text to the screen
        screen.blit(pause, (game_settings.screen_width / 2 - (pause_rect[2] / 2), 150))
        screen.blit(save_game, (game_settings.screen_width / 2 - (save_game_rect[2] / 2), 300))
        screen.blit(settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 340))
        screen.blit(main_menu, (game_settings.screen_width / 2 - (main_menu_rect[2] / 2), 380))
        screen.blit(exit_game, (game_settings.screen_width / 2 - (exit_game_rect[2] / 2), 420))

        # draw the updated screen
        pygame.display.update()

        clock.tick(game_settings.FPS)


def create_user(screen, game_settings):


    screenSize(game_settings.screen_width, game_settings.screen_height)
    setBackgroundImage('img/bg.jpg')

    titleLabel = makeLabel("New Player Registration", 80, 100, 100, game_settings.color_black,
                           game_settings.font, "clear")
    showLabel(titleLabel)

    instructionLabel = makeLabel("Player Name: ", 40, 100, 250, game_settings.color_black,
                                 game_settings.font, "clear")
    showLabel(instructionLabel)  # makes label appear on the screen
    # parameters are in the order x,y,case,prompt,maxlen of characters that can be typed, font size
    # if max len set to 0 any amount of characters can be typed
    wordBox = makeTextBox(420, 250, 300, 0, "Enter text here", 30, 24)
    showTextBox(wordBox)  # makes the text box appear on the screen
    entry = textBoxInput(wordBox)  # user input will be stored in entry

    print(type(entry))
    new_user = User(entry)
    new_user.save()
    pygame.display.update()


def saved_user(screen, game_settings):
    background = pygame.image.load("img/bg.jpg")

    saved = 0
    while True:

        screen.blit(background, (0, 0))
        # creating player instruction
        instructions = text_format("Please Select Gamer Name to Save:", game_settings.font, 60,
                                   game_settings.color_black)
        instructions_rect = instructions.get_rect()
        screen.blit(instructions, (game_settings.screen_width / 3 - (instructions_rect[2] / 3), 125))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_RETURN:
                    saved = 1

        if saved == 1:
            save_confirmation = text_format("<User> progress was successfully saved.", game_settings.font,
                                            40, game_settings.color_white)
            save_confirmation_rect = save_confirmation.get_rect()
            screen.blit(save_confirmation, (game_settings.screen_width / 3 - (save_confirmation_rect[2] / 3),
                                            600))

        pygame.display.update()


def load_user(screen, game_settings, userList):  # user_info
    background = pygame.image.load("img/bg.jpg")

    while True:
        screen.blit(background, (0, 0))

        # creating player instruction
        instructions = text_format("Please Select Gamer Name to Load:", game_settings.font, 60,
                                   game_settings.color_black)
        instructions_rect = instructions.get_rect()
        screen.blit(instructions, (game_settings.screen_width / 3 - (instructions_rect[2] / 3), 115))

        '''
        pixel_space = 240
        for user in userList:
            load_gamer = text_format(user, game_settings.font, 45, game_settings.color_black)
            load_gamer_rect = instructions.get_rect()
            screen.blit(load_gamer, (game_settings.screen_width / 2 - (load_gamer_rect[2] / 2), pixel_space))
            pixel_space += 40
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_RETURN:
                    pass

        pygame.display.update()
