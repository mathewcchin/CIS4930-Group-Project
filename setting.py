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

        # screen settings
        self.caption = "Zombie Apocalypse"
        self.screen_width = 1366
        self.screen_height = 768

        # player settings
        self.character_speed = 3
        self.character_acceleration_ratio = 5
        self.max_health_point = 100
        self.max_health_bar_length = 200
        self.allowed_margin = 20  # minimum allowed distance of player to edge 

        # bullet_pistol settings
        self.bullet_pistol_speed = 50
        self.pistol_shooting_interval = 300  # shooting interval of pistol, in ms

        # weapon and ammo settings
        self.pistol = 0
        self.initial_pistol_ammo = 100
        self.pistol_clip_capacity = 12
        self.pistol_reload_speed = 70  # number of frames to reload
        self.pistol_ammo_life = 200  # number of frames pistol ammo stay on screen
        self.pistol_ammo_drop_rate = 10  # percentage of pistol ammo drop rate
        self.pistol_ammo_min_amount = 5  # minimum pistol bullets per drop
        self.pistol_ammo_max_amount = 25  # maximum pistol bullets per drop

        self.max_reload_bar_length = 60

        self.pistol_sound_path = 'sfx/weapons/p228.wav'
        self.clip_empty_sound_path = 'sfx/weapons/w_empty.wav'
        self.clip_change_sound_path = 'sfx/weapons/clip_change.wav'
        self.ammo_pickup_sound_path = 'sfx/weapons/ammo.wav'
        self.item_pickup_sound_path = 'sfx/weapons/pickup.wav'
        self.ammo_pistol_image_path = 'img/ammo_pistol.png'

        # first_aid_pack settings
        self.first_aid_pack_image_path = 'img/first_aid_pack2.png'
        self.first_aid_pack_life = 200  # number of frames first aid pack stay on screen
        self.first_aid_min_amount = 10  # minimum heal amount of the pack
        self.first_aid_max_amount = 25  # maximum heal amount of the pack
        self.first_aid_pack_drop_rate = 55  # percentage of first aid pack drop rate

        # zombie settings
        self.zombie_image = "img/zombie.png"
        self.zombie_death_sheet_1 = ["img/zombie_death/death_1/6.png", "img/zombie_death/death_1/5.png",
                                     "img/zombie_death/death_1/4.png", "img/zombie_death/death_1/3.png",
                                     "img/zombie_death/death_1/2.png", "img/zombie_death/death_1/1.png"]

        self.zombie_death_sheet_2 = ["img/zombie_death/death_2/6.png", "img/zombie_death/death_2/5.png",
                                     "img/zombie_death/death_2/4.png", "img/zombie_death/death_2/3.png",
                                     "img/zombie_death/death_2/2.png", "img/zombie_death/death_2/1.png"]

        self.zombie_death_sheet_3 = ["img/zombie_death/death_3/10.png",
                                     "img/zombie_death/death_3/9.png", "img/zombie_death/death_3/8.png", "img/zombie_death/death_3/7.png",
                                     "img/zombie_death/death_3/6.png", "img/zombie_death/death_3/5.png", "img/zombie_death/death_3/4.png",
                                     "img/zombie_death/death_3/3.png", "img/zombie_death/death_3/2.png", "img/zombie_death/death_3/1.png"]

        self.zombie_death_frame_multiplier = 3
        self.zombie_corpse_display_frame = 200  # how many frames to keep corpse of zombie

        self.zombie_speed = 3
        self.spawn_distance = 0  # distance to edge of screen, zombies are spawned outside of screen
        self.spawn_time = 1500  # time to spawn a zombie, in milliseconds

        self.zombie_damage = 20  # max damage to player's hp (each attack)
        self.zombie_attack_interval = 1000  # attack time interval, in ms

        # sound channels (playback channels)
        self.foot_step_channel = 0
        self.pistol_channel = 1
        self.zombie_attack_channel = 3

        # welcome menu and game settings
        self.FPS = 60

        # Colors
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)


