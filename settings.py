class Settings():
    """ A class for storing Alien Invasion settings."""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ships_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (160, 160, 230)
        self.bullets_allowed = 4

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10


        # How quickly the game speeds up
        self.speedup_scale = 1.09  # Down from 1.1 to try to make it possible to play as it becomes difficult quickly
        self.score_scale = 1.5

        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        """Initialize settings that changes throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
