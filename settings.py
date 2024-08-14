class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1100  # Screen width in pixels.
        self.screen_height = 600  # Screen height in pixels.
        self.bg_color = (230, 230, 230)  # Background color of the screen.

        # Ship settings.
        self.ship_speed = 1.5  # Speed of the ship.

        # Bullet settings
        self.bullet_speed = 2.0  # Speed of the bullets.
        self.bullet_width = 3  # Width of each bullet.
        self.bullet_height = 15  # Height of each bullet.
        self.bullet_color = (60, 60, 60)  # Color of the bullets.
        self.bullets_allowed = 3  # Maximum number of bullets allowed on the screen.
         
        #Alien Setting:
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    