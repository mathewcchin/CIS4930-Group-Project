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

        # screen settings
        self.caption = "Zombie Apocalypse"
        self.screen_width = 1366
        self.screen_height = 768

        # main character settings (carrying pistol)
        self.character_speed = 3
        self.character_acceleration_ratio = 5
        self.max_health_point = 200
        self.allowed_margin = 20  # minimum allowed distance of player to edge 

        # zombie settings
        self.zombie_image = "img/zombie.png"
        self.zombie_death_sheet_1 = ["img/zombie_death/death_1/6.png", "img/zombie_death/death_1/5.png",
                                     "img/zombie_death/death_1/4.png", "img/zombie_death/death_1/3.png",
                                     "img/zombie_death/death_1/2.png", "img/zombie_death/death_1/1.png"]

        self.zombie_death_sheet_2 = ["img/zombie_death/death_2/6.png", "img/zombie_death/death_2/5.png",
                                     "img/zombie_death/death_2/4.png", "img/zombie_death/death_2/3.png",
                                     "img/zombie_death/death_2/2.png", "img/zombie_death/death_2/1.png"]

        self.zombie_death_sheet_3 = ["img/zombie_death/death_3/15.png", "img/zombie_death/death_3/14.png", "img/zombie_death/death_3/13.png",
                                     "img/zombie_death/death_3/12.png", "img/zombie_death/death_3/11.png", "img/zombie_death/death_3/10.png",
                                     "img/zombie_death/death_3/9.png", "img/zombie_death/death_3/8.png", "img/zombie_death/death_3/7.png",
                                     "img/zombie_death/death_3/6.png", "img/zombie_death/death_3/5.png", "img/zombie_death/death_3/4.png",
                                     "img/zombie_death/death_3/3.png", "img/zombie_death/death_3/2.png", "img/zombie_death/death_3/1.png"]

        # self.zombie_death_sheet_3 = ["img/zombie_death/death_3/15.png", "img/zombie_death/death_3/14.png", "img/zombie_death/death_3/13.png",
        #                              "img/zombie_death/death_3/12.png", "img/zombie_death/death_3/11.png", "img/zombie_death/death_3/10.png",
        #                              "img/zombie_death/death_3/9.png"]

        self.zombie_death_frame_multiplier = 5
        self.zombie_corpse_display_frame = 1000  # how many frames to keep corpse of zombie

        self.zombie_speed = 3
        self.spawn_distance = 0  # distance to edge of screen, zombies are spawned outside of screen
        self.spawn_time = 1500  # time to spawn a zombie, in milliseconds

        self.zombie_damage = 20  # max damage to player's hp (each attack)
        self.zombie_attack_interval = 1000  # attack time interval, in ms

        # bullet_pistol settings
        self.bullet_pistol_speed = 80
        self.pistol_shooting_interval = 300  # shooting interval of pistol, in ms

        # sound channels (playback channels)
        self.foot_step_channel = 0
        self.pistol_channel = 1
        self.zombie_hit_channel = 3

        # welcome menu and game settings
        self.font = "img/INVASION2000.TTF"
        self.FPS = 60

        # Colors
        self.color_white = (255, 255, 255)
        self.color_black = (0, 0, 0)


