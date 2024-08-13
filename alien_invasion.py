import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # Initialize all imported pygame modules.
        self.clock = pygame.time.Clock()  # Create a Clock object to manage frame rate.
        self.settings = Settings()  # Create an instance of the Settings class.

        # Set up the screen with dimensions from settings.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")  # Set the window title.

        # Create an instance of the Ship class.
        self.ship = Ship(self)
        # Create a group to hold and manage bullets.
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # Check for any events such as key presses.
            self.ship.update()  # Update the ship's position based on movement flags.
            self._update_bullets()  # Update bullet positions and remove old bullets.
            self._update_screen()  # Update the screen with the latest images.
            self.clock.tick(60)  # Limit the frame rate to 60 frames per second.

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():  # Get a list of all events.
            if event.type == pygame.QUIT:
                sys.exit()  # Exit the game if the quit event is detected.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  # Check for key press events.
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  # Check for key release events.

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # Set the flag to move the ship right.
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True  # Set the flag to move the ship left.
        elif event.key == pygame.K_q:
            sys.exit()  # Exit the game if 'q' is pressed.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # Fire a bullet if the spacebar is pressed.

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False  # Stop moving right when the key is released.
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False  # Stop moving left when the key is released.

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)  # Create a new Bullet instance.
            self.bullets.add(new_bullet)  # Add the new bullet to the bullets group.

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()  # Update the position of all bullets.

        # Remove bullets that have moved off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # Fill the screen with the background color.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # Draw each bullet on the screen.
        self.ship.blitme()  # Draw the ship on the screen.

        pygame.display.flip()  # Make the most recently drawn screen visible.

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
