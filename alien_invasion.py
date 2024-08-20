import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from game_stats import GameStats
from alien import Alien
from button import Button
from scoreboard import ScoreBoard


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
        
        #Create an instance to store the game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb    = ScoreBoard(self)
        #Start the game in an inactive state.
        self.game_active = False
        # Create an instance of the Ship class.
        self.ship = Ship(self)
        # Create a group to hold and manage bullets.
        self.bullets = pygame.sprite.Group()
        #Create a group to hold and manage aliens
        self.aliens  = pygame.sprite.Group()
        self._create_fleet()
        # Make the play button.
        self.play_button = Button(self,"Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # Check for any events such as key presses.
            if self.game_active:
              self.ship.update()  # Update the ship's position based on movement flags.
              self._update_bullets()  # Update bullet positions and remove old bullets.
              self._update_aliens()   #Update aliens position to the right
              
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        
        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        '''Respond to bullet and aliens collisions'''
        # Check for any bullet that has hit the aliens
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
        #Creating a new fleet of aliens once the previous fleet is completely destroyed.
        if not self.aliens:
            #Destroy existing bullets and create the new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
  
    def _create_fleet(self):
        '''Create the fleet of the alien'''
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value and increment the y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self,x_position,y_position):
        '''Create an alien and place it in the row'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _change_fleet_direction(self):
      """Drop the entire fleet and change the fleet's direction."""
      for alien in self.aliens.sprites():
         alien.rect.y += self.settings.fleet_drop_speed
      self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        '''Respond appropriately if any aliens have reached the edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions:
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
        

    def _check_aliens_bottom(self):
        '''Check if any alien has reached the bottom of the screen'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if ship gets hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        '''Respond to the ship being hit by the aliens'''
        if self.stats.ships_left > 0:
           # Decrement the ships left.
           self.stats.ships_left -= 1
           # Get rid of any remaining bullets and aliens.
           self.bullets.empty()
           self.aliens.empty()
           # Create a new fleet and center the ship.
           self._create_fleet()
           self.ship.center_ship()
           #Pause
           sleep(0.5)
        else:
            self.game_active = False
            # Show the mouse cursor again.
            pygame.mouse.set_visible(True)


    def _check_play_button(self,mouse_pos):
        '''Start a new game when the player click the play button'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Reset the game speed to initial speed.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True
            self.sb.prep_score()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # Fill the screen with the background color.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # Draw each bullet on the screen.
        self.ship.blitme()  # Draw the ship on the screen.
        self.aliens.draw(self.screen) #Draw the alien on the screen
        self.sb.show_score() #Draw the score information.
        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # Make the most recently drawn screen visible.
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
