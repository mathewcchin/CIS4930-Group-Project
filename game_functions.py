from pygame.sprite import Group  # for grouping multiple objects based on pygame.sprite
from player import Player
from zombie import *
from ammo import *
from first_aid_pack import *
from player_resources import PlayerResources
from userinfo import User
from user_registration import *
import pickle
import os


def run_game(screen, game_settings, username):
    """
    This function does following:
        -Initialize game objects
        -create a screen object
        -run the main game loop
        -deal with after-exiting tasks

    :return: Null
    """

    # create objects that will displayed on game main screen
    background = pygame.image.load(game_settings.background_path).convert_alpha()

    # create Group() objects to store game objects shown on screen
    bullets = Group()
    zombies = Group()
    last_spawn_time = pygame.time.get_ticks()  # record zombie spawn time
    dead_zombies = Group()
    ammos = Group()
    first_aid_packs = Group()

    # player object
    player_resources = PlayerResources(game_settings)
    player = Player(screen, game_settings, bullets, player_resources)

    # controls game fps
    clock = pygame.time.Clock()

    # start the main loop of the game
    while True:
        # FPS
        clock.tick(game_settings.FPS)

        # check event
        check_events(player, bullets, game_settings, screen, username)

        # generate zombies
        last_spawn_time = spawn_zombies(zombies, player, game_settings, screen, last_spawn_time)

        # delete zombies and bullets when zombie is shot by bullet
        shoot_zombie(zombies, bullets, dead_zombies, player, ammos, first_aid_packs)

        # zombie attack player
        attack_player(zombies, player)

        # player get item
        player_get_item(player, ammos, first_aid_packs)

        # update game objects
        player.update()  # player's rotation and position
        zombies.update()  # zombie's rotation and position
        dead_zombies.update()  # decrease remaining frames of corpse display
        bullets.update()  # bullets' rotation and position
        ammos.update()  # decrease remaining frames of ammos
        first_aid_packs.update()  # decrease remaining frames of first-aid-pack

        # update screen
        update_screen(background, player, zombies, screen, bullets, dead_zombies, ammos, first_aid_packs)

        # if player is dead, break the main game loop
        if player.hp <= 0:
            break

        # check how many zombies player killed, increase difficulty
        if player.zombie_killed > 120:
            game_settings.spawn_time = 500
        elif player.zombie_killed > 75:
            game_settings.spawn_time = 1000
        elif player.zombie_killed > 25:
            game_settings.spawn_time = 1500
        elif player.zombie_killed > 10:
            game_settings.spawn_time = 2500


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

    if event.key == pygame.K_r:
        # reload
        if player.current_weapon == player.game_settings.pistol and player.clip_pistol < player.game_settings.pistol_clip_capacity and player.ammo_pistol > 0:
            player.reload()

        if player.current_weapon == player.game_settings.m4 and player.clip_m4 < player.game_settings.m4_clip_capacity and player.ammo_m4 > 0:
            player.reload()

        if player.current_weapon == player.game_settings.awp and player.clip_awp < player.game_settings.awp_clip_capacity and player.ammo_awp > 0:
            player.reload()

    if event.key == pygame.K_1:
        # change weapon to pistol
        if player.reload_frame == 0:
            player.current_weapon = player.game_settings.pistol

    if event.key == pygame.K_2:
        # change weapon to m4
        if player.reload_frame == 0:
            player.current_weapon = player.game_settings.m4

    if event.key == pygame.K_3:
        # change weapon to m4
        if player.reload_frame == 0:
            player.current_weapon = player.game_settings.awp


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


def check_mousedown(event, player):
    """
    Parameter:
        player: used to calculate the position and angle of the bullet
        bullets: will add bullet to this group, if left mouse clicked
    """

    # left click
    if event.button == 1:
        player.fire()

    # wheel scroll forward: change weapon
    if event.button == 4 and player.reload_frame == 0:
        player.current_weapon = (player.current_weapon + 1) % player.game_settings.weapon_number

    # wheel scroll forward: change weapon
    if event.button == 5 and player.reload_frame == 0:
        player.current_weapon = (player.current_weapon - 1) % player.game_settings.weapon_number


def check_mouseup(event, player):
    # left click
    if event.button == 1:
        player.auto_shooting = False
        player.auto_reload_flag = True


def check_events(player, bullets, game_settings, screen, username):
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
                pause_game(screen, game_settings, player, username)

        if event.type == pygame.KEYUP:
            check_keyup_events(event, player)

        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mousedown(event, player)

        if event.type == pygame.MOUSEBUTTONUP:
            check_mouseup(event, player)


def spawn_zombies(zombies, player, game_settings, screen, last_spawn_time):
    # if time interval is less than spawn time, do nothing
    if pygame.time.get_ticks() - last_spawn_time < game_settings.spawn_time:
        return last_spawn_time

    # if time interval is larger than spawn time, create a new zombie in zombies
    new_zombie = Zombie(game_settings, screen, player)
    zombies.add(new_zombie)

    # return new spawn time
    return pygame.time.get_ticks()


def shoot_zombie(zombies, bullets, dead_zombies, player, ammos, first_aid_packs):
    for zombie in zombies.copy().sprites():
        for bullet in bullets.copy().sprites():
            if zombie.rect.colliderect(bullet.rect) and rect_center_distance(bullet.rect,
                                                                             zombie.rect) <= bullet.game_settings.bullet_awp_damage_distance:
                # play the hitting sound effect and count hit
                zombie.hit_channel.play(zombie.zombie_hit_sound)
                if bullet.damage == bullet.original_damage:
                    player.zombie_hit += 1

                # decrease zombie's hp and bullet's damage
                # if bullet damage is zero, remove it
                zm_hp = zombie.hp
                zombie.hp -= bullet.damage  # damage zombie
                zombie.hit_slow_down_factor *= bullet.slow_down_factor  # slow down zombie

                bullet.damage -= zm_hp  # decrease bullet damage and remove weak bullet
                if bullet.damage <= 20:
                    bullets.remove(bullet)

                # check if this zombie died or not
                if zombie.hp <= 0:
                    # play death sound and remove zombie from zombies
                    zombie.hit_channel.play(zombie.zombie_death_sound)
                    zombies.remove(zombie)

                    # create a new dead zombie and add to dead_zombies
                    new_dead_zombie = DeadZombie(zombie)
                    dead_zombies.add(new_dead_zombie)

                    # update player's kill score
                    player.zombie_killed += 1

                    # drop ammo
                    if random.randint(1, 100) <= zombie.game_settings.pistol_ammo_drop_rate:
                        new_ammo = PistolAmmo(zombie)
                        ammos.add(new_ammo)

                    if random.randint(1, 100) <= zombie.game_settings.m4_ammo_drop_rate:
                        new_ammo = M4Ammo(zombie)
                        ammos.add(new_ammo)

                    if random.randint(1, 100) <= zombie.game_settings.awp_ammo_drop_rate:
                        new_ammo = AwpAmmo(zombie)
                        ammos.add(new_ammo)

                    # drop first aid pack
                    if random.randint(1, 100) <= zombie.game_settings.first_aid_pack_drop_rate:
                        new_first_aid_pack = FirstAidPack(zombie)
                        first_aid_packs.add(new_first_aid_pack)


def rect_center_distance(rect_a, rect_b):
    return math.sqrt(pow((rect_a.centerx - rect_b.centerx), 2) + pow((rect_a.centery - rect_b.centery), 2))


def attack_player(zombies, player):
    for zombie in zombies.sprites():
        if zombie.rect.colliderect(
                player.rect) and pygame.time.get_ticks() - zombie.last_attacking_time >= player.game_settings.zombie_attack_interval:
            # attack player
            zombie.attack_player(player)


def update_screen(background, player, zombies, screen, bullets, dead_zombies, pistol_ammos, first_aid_packs):
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

    # draw each ammo to screen, remove those expired
    for pistol_ammo in pistol_ammos.copy().sprites():
        if pistol_ammo.ammo_life <= 0:
            pistol_ammos.remove(pistol_ammo)
        else:
            pistol_ammo.blit_ammo()

    # draw each first aid pack to screen, remove those expired
    for first_aid_pack in first_aid_packs.copy().sprites():
        if first_aid_pack.pack_life <= 0:
            first_aid_packs.remove(first_aid_pack)
        else:
            first_aid_pack.blit_pack()

    # draw each zombie to screen
    for zombie in zombies:
        zombie.blit_zombie()

    # draw player's character to screen
    player.blit_player()

    # draw the updated screen on the game window
    pygame.display.flip()


def player_get_item(player, ammos, first_aid_packs):
    # get pistol ammos
    for ammo in ammos.copy().sprites():
        if player.rect.colliderect(ammo.rect):
            if ammo.ammo_type == player.game_settings.pistol:
                player.ammo_pistol += ammo.amount
            if ammo.ammo_type == player.game_settings.m4:
                player.ammo_m4 += ammo.amount
            if ammo.ammo_type == player.game_settings.awp:
                player.ammo_awp += ammo.amount

            player.foot_steps_channel.play(player.ammo_pickup_sound)  # play sound
            ammos.remove(ammo)

    # get first aid packs
    for first_aid_pack in first_aid_packs.copy().sprites():
        if player.rect.colliderect(first_aid_pack.rect):
            # heal player
            player.hp += first_aid_pack.heal_amount
            if player.hp > player.game_settings.max_health_point:
                player.hp = player.game_settings.max_health_point
            # play sound effect
            player.foot_steps_channel.play(player.item_pickup_sound)
            # delete pack
            first_aid_packs.remove(first_aid_pack)


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

                elif selected == "leaderboard" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "load game"

                elif selected == "settings" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "leaderboard"

                elif selected == "quit" and event.key == pygame.K_UP:
                    key_sound.play()
                    selected = "settings"

                elif selected == "new game" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "load game"

                elif selected == "load game" and event.key == pygame.K_DOWN:
                    key_sound.play()
                    selected = "leaderboard"

                elif selected == "leaderboard" and event.key == pygame.K_DOWN:
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
                        username = create_user(screen, game_settings)
                        run_game(screen, game_settings, username)
                    if selected == "load game":
                        load_user(screen, game_settings)
                    if selected == "leaderboard":
                        leaderboard(screen, game_settings)
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
        if selected == "leaderboard":
            text_leaderboard = text_format("LEADERBOARD", font, 75, game_settings.color_white)
        else:
            text_leaderboard = text_format("LEADERBOARD", font, 75, game_settings.color_black)
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
        leaderboard_rect = text_leaderboard.get_rect()
        settings_rect = text_settings.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (game_settings.screen_width / 2 - (title_rect[2] / 2), 150))
        screen.blit(text_new_game, (game_settings.screen_width / 2 - (new_game_rect[2] / 2), 300))
        screen.blit(text_load_game, (game_settings.screen_width / 2 - (load_game_rect[2] / 2), 350))
        screen.blit(text_leaderboard, (game_settings.screen_width / 2 - (leaderboard_rect[2] / 2), 400))
        screen.blit(text_settings, (game_settings.screen_width / 2 - (settings_rect[2] / 2), 450))
        screen.blit(text_quit, (game_settings.screen_width / 2 - (quit_rect[2] / 2), 500))
        pygame.display.update()
        clock.tick(FPS)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def user_settings(screen, game_settings):
    # create objects that will displayed on game main screen
    background = pygame.image.load(game_settings.background_path)

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


def pause_game(screen, game_settings, player, username):
    # draws background
    background = pygame.image.load(game_settings.background_path)

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
                        saved_user(screen, game_settings, player, username)
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
    setBackgroundImage(game_settings.background_path)

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

    new_user = User()
    if new_user.check_user(entry) == 1:
        create_user(screen, game_settings)

    else:
        addtoleadtable(entry, 0)
        savegame(entry, new_user)

    pygame.display.update()

    return entry


def saved_user(screen, game_settings, player, user):
    background = pygame.image.load(game_settings.background_path)

    saved = 0
    temp_user = User()

    while True:
        screen.blit(background, (0, 0))

        # creating player instruction
        instructions = text_format("Press Enter to Save progress:", game_settings.font, 60,
                                   game_settings.color_black)
        instructions_rect = instructions.get_rect()
        screen.blit(instructions, (game_settings.screen_width / 3 - (instructions_rect[2] / 3), 125))
        load_gamer = text_format(user, game_settings.font, 45, game_settings.color_black)
        load_gamer_rect = instructions.get_rect()
        screen.blit(load_gamer, (game_settings.screen_width / 2 - (load_gamer_rect[2] / 2), 240))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_RETURN:
                    saved = 1
                    existing_user = loadgame(user, temp_user)
                    existing_user.add_score(player.zombie_killed)
                    addtoleadtable(user, existing_user.show_score())
                    savegame(user, temp_user)
        if saved == 1:
            save_confirmation = text_format(user + " progress was successfully saved.",
                                            game_settings.font, 40, game_settings.color_white)
            save_confirmation_rect = save_confirmation.get_rect()
            screen.blit(save_confirmation, (game_settings.screen_width / 3 - (save_confirmation_rect[2] / 3),
                                          600))

        pygame.display.update()


def load_user(screen, game_settings):  # user_info

    screenSize(game_settings.screen_width, game_settings.screen_height)
    setBackgroundImage(game_settings.background_path)
    instruction = makeLabel("Please ENTER Gamer Name to Load: ", 50, 100, 100, game_settings.color_black,
                                 game_settings.font, "clear")
    showLabel(instruction)

    username = User()
    userList = username.show_users()

    pixel_x_size = 100
    pixel_y_size = 240
    for user in userList:
        if pixel_y_size >= 500:
            pixel_x_size += 250
            pixel_y_size = 240
            display_user = makeLabel(user, 40, pixel_x_size, pixel_y_size, game_settings.color_black,
                                     game_settings.font, "clear")
            showLabel(display_user)

            pixel_y_size += 60

        else:
            display_user = makeLabel(user, 40, pixel_x_size, pixel_y_size, game_settings.color_black,
                                     game_settings.font, "clear")
            showLabel(display_user)

            pixel_y_size += 60


    instructionLabel = makeLabel("Player Name: ", 40, 100, 600, game_settings.color_black,
                                 game_settings.font, "clear")
    showLabel(instructionLabel)  # makes label appear on the screen
    # parameters are in the order x,y,case,prompt,maxlen of characters that can be typed, font size
    # if max len set to 0 any amount of characters can be typed
    wordBox = makeTextBox(420, 600, 300, 0, "Enter text here", 30, 24)
    showTextBox(wordBox)  # makes the text box appear on the screen
    entry = textBoxInput(wordBox)  # user input will be stored in entry

    name = User()
    if name.check_user(entry):
        run_game(screen, game_settings, entry)

    else:
        load_user(screen, game_settings)

    pygame.display.update()


def leaderboard(screen, game_settings):  # user_info
    background = pygame.image.load("img/bg.jpg")
    leadtable = openleadtable()
    while True:
        screen.blit(background, (0, 0))
        # creating player instruction
        instructions = text_format("Leaderboard:", game_settings.font, 100,
                                   game_settings.color_black)
        instructions_rect = instructions.get_rect()
        screen.blit(instructions, (game_settings.screen_width / 6 - (instructions_rect[2] / 6), 115))
        pixel_space = 240
        count =0
        for key, value in sorted(leadtable.items(), key = lambda kv:(kv[1],kv[0]), reverse=True):
            if(count <=4):
                statement = str(count+1)+".  "+key + "  . . . . . . . . . . " + str(value)
                load_gamer = text_format(statement, game_settings.font, 60, game_settings.color_black)
                load_gamer_rect = instructions.get_rect()
                screen.blit(load_gamer, (game_settings.screen_width / 6 - (load_gamer_rect[2] / 6), pixel_space))
                pixel_space += 60
                count+=1
            else:
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    pass

            pygame.display.update()


def savegame(filetag, user):
    current_dir = os.getcwd() + "/users"
    file_to_open = os.path.join(current_dir, (filetag + ".dat"))
    user_file = open(file_to_open, "wb")
    pickle.dump(user, user_file)
    user_file.close()


def loadgame(filetag, user):
    file = os.path.join((os.getcwd() + "/users"), filetag + ".dat")
    pickle_in = open(file, "rb")
    user = pickle.load(pickle_in)
    return user


def saveleadtable(leadtable):
    file = open("leaderboard.dat", "wb")
    pickle.dump(leadtable, file)
    file.close()


def openleadtable():
    pickle_in = open("leaderboard.dat", "rb")
    table = pickle.load(pickle_in)
    return table


def addtoleadtable(name, score):
    '''file = os.getcwd() + "leaderboard.dat"
    if "leaderboard.dat" != file:
        x = dict({name: score})
        saveleadtable(x)
    else:'''
    y = openleadtable()
    y.update({name: score})
    saveleadtable(y)
