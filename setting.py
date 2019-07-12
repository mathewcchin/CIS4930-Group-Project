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
        self.caption = "shooting game test"
        self.screen_width = 1280
        self.screen_height = 720

        # main character settings (carrying pistol)
        self.character_speed = 3
        self.character_acceleration_ratio = 5
        self.max_health_point = 200

        # enemy settings
        self.enemy_speed = 3
        self.enemy_timer = 100
        self.enemy_timer_1 = 0

        # bullet_pistol settings
        self.bullet_pistol_speed = 40

        # sound channels (playback channels)
        self.foot_step_channel = 0
        self.pistol_channel = 1

        # other game settings
        self.total_time = 90

        # welcome menu settings
        self.font = "img/INVASION2000.TTF"
