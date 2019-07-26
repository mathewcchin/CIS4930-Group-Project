class Settings:
    """
    A class to store all settings for the game. For easy modifying

    Attributes (self.):
        :caption: title of the game window
        :screen_width: size of the game window
        :screen_height: size of the game window

        :character_speed:
            The speed of the character. Increase step size of char's rect during
            each game loop.
        :character_acceleration_ratio:
            Maximum acceleration ratio (times of self.character_speed
        :max_health_point:
            Maximum health point of player's character

        :enemy_speed: speed of enemy (zombies)
        :enemy_timer:
        :enemy_timer_1: two timers used to control the time and frequency
            of enemy's occurrence

        :total_time: the total time one game lasts
    """

    def __init__(self):
        """initialize game setting attributes"""

        # fonts
        self.digital_font_path = "fonts/DS-DIGIT.TTF"
        self.font = "img/INVASION2000.TTF"
        self.segoeui_path = "fonts/segoeui.ttf"

        # screen settings
        self.caption = "Zombie Apocalypse"
        self.screen_width = 1366
        self.screen_height = 768

        # UI settings
        self.background_path = 'img/bg.png'
        self.health_bar_distancex = 350  # distance to x = screen.width (x-direction)
        self.health_bar_distancey = 40  # distance to y = screen.height (y-direction)
        self.weapon_distancex = 200  # distance to x = 0 (x-direction)
        self.weapon_distancey = 50  # distance to y = screen.height (y-direction)

        # player settings and resources
        self.character_speed = 4
        self.weapon_speed_reduce_factor = (0, 1, 2)  # check weapon_number and weapon id for detail. This is speed decrease when player carrying specific type of weapon
        self.weapon_foot_step_interval = (350, 500, 700)
        self.max_health_point = 100
        self.max_health_bar_length = 200
        self.allowed_margin = 45  # minimum allowed distance of player to edge

        self.player_pistol_image_path = 'img/player_pistol.png'
        self.player_m4_image_path = 'img/player_m4.png'
        self.player_awp_image_path = 'img/player_awp.png'
        self.player_health_icon_path = 'img/health.png'

        self.foot_step_sound1_path = 'sfx/character/pl_step1.wav'
        self.foot_step_sound2_path = 'sfx/character/pl_step2.wav'
        self.foot_step_sound3_path = 'sfx/character/pl_step3.wav'
        self.foot_step_sound4_path = 'sfx/character/pl_step4.wav'

        # bullet_pistol settings
        self.bullet_pistol_image_path = "img/bullet_pistol.png"
        self.bullet_pistol_speed = 50
        self.pistol_shooting_interval = 250  # shooting interval of pistol, in ms
        self.bullet_pistol_min_damage = 30
        self.bullet_pistol_max_damage = 55
        self.bullet_pistol_slow_down_factor = 0.6  # will slow down zombie to this ratio

        # bullet_m4 settings
        self.bullet_m4_image_path = "img/bullet_m4.png"
        self.bullet_m4_speed = 100
        self.m4_shooting_interval = 130  # shooting interval of pistol, in ms
        self.bullet_m4_min_damage = 55
        self.bullet_m4_max_damage = 110
        self.bullet_m4_slow_down_factor = 0.4  # will slow down zombie to this ratio

        # bullet_awp settings
        self.bullet_awp_image_path = "img/bullet_awp.png"
        self.bullet_awp_speed = 120
        self.awp_shooting_interval = 1500  # shooting interval of pistol, in ms
        self.bullet_awp_min_damage = 500
        self.bullet_awp_max_damage = 700
        self.bullet_awp_damage_distance = 80  # center distance between bullet's rect and target's rect
        self.bullet_awp_slow_down_factor = 0.2  # will slow down zombie to this ratio

        # weapon and ammo settings and resources
        self.weapon_number = 3
        self.pistol = 0
        self.m4 = 1
        self.awp = 2

        self.initial_pistol_ammo = 100
        self.pistol_clip_capacity = 12
        self.pistol_reload_speed = 40  # number of frames to reload
        self.pistol_ammo_life = 600  # number of frames pistol ammo stay on screen
        self.pistol_ammo_drop_rate = 10  # percentage
        self.pistol_ammo_min_amount = 15  # minimum pistol bullets per drop
        self.pistol_ammo_max_amount = 25  # maximum pistol bullets per drop
        self.pistol_fire_frame_multiplier = 1  # multiplier for each frame, to extend length

        self.initial_m4_ammo = 30
        self.m4_clip_capacity = 30
        self.m4_reload_speed = 70  # number of frames to reload
        self.m4_ammo_life = 600  # number of frames m4 ammo stay on screen
        self.m4_ammo_drop_rate = 3  # percentage
        self.m4_ammo_min_amount = 20  # minimum m4 bullets per drop
        self.m4_ammo_max_amount = 40  # maximum m4 bullets per drop
        self.m4_fire_frame_multiplier = 1  # multiplier for each frame, to extend length

        self.initial_awp_ammo = 20
        self.awp_clip_capacity = 10
        self.awp_reload_speed = 90  # number of frames to reload
        self.awp_ammo_life = 600  # number of frames awp ammo stay on screen
        self.awp_ammo_drop_rate = 1  # percentage
        self.awp_ammo_min_amount = 12  # minimum awp bullets per drop
        self.awp_ammo_max_amount = 20  # maximum awp bullets per
        self.awp_fire_frame_multiplier = 1  # multiplier for each frame, to extend length

        self.max_reload_bar_length = 60

        self.pistol_sound_path = 'sfx/weapons/usp.wav'
        self.pistol_reload_sound_path = 'sfx/weapons/reload_pistol.wav'
        self.ammo_pistol_image_path = 'img/ammo_pistol.png'
        self.pistol_image_path = 'img/pistol.png'
        self.pistol_fire_frame_paths = ('img/player_fire_sheet/pistol/pf16.png',
                                        'img/player_fire_sheet/pistol/pf15.png',
                                        'img/player_fire_sheet/pistol/pf14.png',
                                        'img/player_fire_sheet/pistol/pf13.png',
                                        'img/player_fire_sheet/pistol/pf12.png',
                                        'img/player_fire_sheet/pistol/pf11.png',
                                        'img/player_fire_sheet/pistol/pf10.png',
                                        'img/player_fire_sheet/pistol/pf9.png',
                                        'img/player_fire_sheet/pistol/pf8.png',
                                        'img/player_fire_sheet/pistol/pf7.png',
                                        'img/player_fire_sheet/pistol/pf6.png',
                                        'img/player_fire_sheet/pistol/pf5.png',
                                        'img/player_fire_sheet/pistol/pf4.png',
                                        'img/player_fire_sheet/pistol/pf3.png',
                                        'img/player_fire_sheet/pistol/pf2.png',
                                        'img/player_fire_sheet/pistol/pf1.png',
                                        )

        self.m4_sound_path = 'sfx/weapons/m4a1.wav'
        self.m4_reload_sound_path = 'sfx/weapons/reload_m4.wav'
        self.ammo_m4_image_path = 'img/ammo_m4.png'
        self.m4_image_path = 'img/m4.png'
        self.m4_fire_frame_paths = ('img/player_fire_sheet/m4/mf16.png',
                                    'img/player_fire_sheet/m4/mf15.png',
                                    'img/player_fire_sheet/m4/mf14.png',
                                    'img/player_fire_sheet/m4/mf13.png',
                                    'img/player_fire_sheet/m4/mf12.png',
                                    'img/player_fire_sheet/m4/mf11.png',
                                    'img/player_fire_sheet/m4/mf10.png',
                                    'img/player_fire_sheet/m4/mf9.png',
                                    'img/player_fire_sheet/m4/mf8.png',
                                    'img/player_fire_sheet/m4/mf7.png',
                                    'img/player_fire_sheet/m4/mf6.png',
                                    'img/player_fire_sheet/m4/mf5.png',
                                    'img/player_fire_sheet/m4/mf4.png',
                                    'img/player_fire_sheet/m4/mf3.png',
                                    'img/player_fire_sheet/m4/mf2.png',
                                    'img/player_fire_sheet/m4/mf1.png',
                                    )

        self.awp_sound_path = 'sfx/weapons/awp.wav'
        self.awp_reload_sound_path = 'sfx/weapons/reload_awp.wav'
        self.ammo_awp_image_path = 'img/ammo_awp.png'
        self.awp_image_path = 'img/awp.png'
        self.awp_fire_frame_paths = ('img/player_fire_sheet/awp/af16.png',
                                     'img/player_fire_sheet/awp/af15.png',
                                     'img/player_fire_sheet/awp/af14.png',
                                     'img/player_fire_sheet/awp/af13.png',
                                     'img/player_fire_sheet/awp/af12.png',
                                     'img/player_fire_sheet/awp/af11.png',
                                     'img/player_fire_sheet/awp/af10.png',
                                     'img/player_fire_sheet/awp/af9.png',
                                     'img/player_fire_sheet/awp/af8.png',
                                     'img/player_fire_sheet/awp/af7.png',
                                     'img/player_fire_sheet/awp/af6.png',
                                     'img/player_fire_sheet/awp/af5.png',
                                     'img/player_fire_sheet/awp/af4.png',
                                     'img/player_fire_sheet/awp/af3.png',
                                     'img/player_fire_sheet/awp/af2.png',
                                     'img/player_fire_sheet/awp/af1.png',
                                     )

        self.clip_empty_sound_path = 'sfx/weapons/w_empty.wav'
        self.ammo_pickup_sound_path = 'sfx/weapons/ammo.wav'
        self.item_pickup_sound_path = 'sfx/weapons/pickup.wav'

        # reload speed
        self.reload_speed = {
            self.pistol: self.pistol_reload_speed,
            self.m4: self.m4_reload_speed,
            self.awp: self.awp_reload_speed,
        }

        # first_aid_pack settings
        self.first_aid_pack_image_path = 'img/first_aid_pack.png'
        self.first_aid_pack_life = 600  # number of frames first aid pack stay on screen
        self.first_aid_min_amount = 45  # minimum heal amount of the pack
        self.first_aid_max_amount = 65  # maximum heal amount of the pack
        self.first_aid_pack_drop_rate = 10  # percentage of first aid pack drop rate

        # zombie settings
        self.zombie_max_health = 100
        self.zombie_max_health_bar_length = 70
        self.zombie_image_path = "img/zombie.png"
        self.zombie_attack_image_path = 'img/zombie_attack.png'
        self.zombie_death_sheet_3 = ["img/zombie_death/death_3/10.png",
                                     "img/zombie_death/death_3/9.png", "img/zombie_death/death_3/8.png", "img/zombie_death/death_3/7.png",
                                     "img/zombie_death/death_3/6.png", "img/zombie_death/death_3/5.png", "img/zombie_death/death_3/4.png",
                                     "img/zombie_death/death_3/3.png", "img/zombie_death/death_3/2.png", "img/zombie_death/death_3/1.png"]

        self.zombie_death_frame_multiplier = 3
        self.zombie_corpse_display_frame = 200  # how many frames to keep corpse of zombie

        self.zombie_speed = 3
        self.spawn_distance = 0  # distance to edge of screen, zombies are spawned outside of screen
        self.spawn_time = 1000  # time to spawn a zombie, in milliseconds

        self.zombie_damage = 20  # max damage to player's hp (each attack)
        self.zombie_attack_interval = 1000  # attack time interval, in ms
        self.zombie_attack_sound_path = ['sfx/zombie/zm_attack1.wav', 'sfx/zombie/zm_attack2.wav', 'sfx/zombie/zm_attack3.wav', 'sfx/zombie/zm_attack4.wav']
        self.zombie_hit_sound_path = 'sfx/zombie/zm_hit.wav'
        self.zombie_death_sound_path = 'sfx/zombie/explode.wav'
        self.zombie_hit_slow_down_restore_factor = 0.02  # amount to restore the zombie hit slow down factor by each frame

        # sound channels (playback channels)
        self.foot_step_channel = 0
        self.gun_channel = 1
        self.zombie_hit_channel = 2
        self.zombie_attack_channel = 3

        # welcome menu and game settings
        self.FPS = 60

        # Colors
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)
        self.BRIGHT_YELLOW = (255, 255, 78)
        self.DARK_GREEN = (64, 184, 76)
        self.DARK_RED = (184, 64, 64)

