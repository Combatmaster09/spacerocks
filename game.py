import pygame
import pygame.mixer
from models import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text, load_sound
import globals

class SpaceRocks:
    """This class represents the main game loop and manages the overall game state"""
    MIN_ASTEROID_DISTANCE = 250
    restart_game = False
    asteroid_count = 1
    def __init__(self):
        """This function initializes the pygame library, screen, clock, font, music, 
        and other game objects"""
        self._init_pygame()
        self.screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT), pygame.FULLSCREEN)
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ' '
        self.music_score = load_sound('WRTC')
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.music_score.play()
        for _ in range(self.asteroid_count):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        """This function is the main game loop that handles user input, 
        game logic processing, and rendering"""
        while globals.game:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            if self.restart_game:
                self.reset_game()
                self.restart_game = False

    def reset_game(self):
        """This function resets the game by clearing asteroids, score, and 
        reinitializing the spaceship and asteroids"""
        self.asteroids.clear()
        self.message = None
        if not self.spaceship:
            globals.score = 0
            self.spaceship = Spaceship((400, 300), self.bullets.append)
            self.asteroid_count = 1
        else:
             globals.score += 1000
             globals.level += 1
             for _ in range(self.asteroid_count):
                while True:
                    position = get_random_position(self.screen)
                    if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                        self.asteroids.append(Asteroid(position, self.asteroids.append))
                        break

    def _init_pygame(self):
        """This function initializes the pygame library and sets the game window caption"""
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        
    def _handle_input(self):
        """This function handles user input from keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and not self.spaceship
            ):
                self.restart_game = True
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RIGHTBRACKET
            ):
                self.asteroid_count = self.asteroid_count * 2
        
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT] or is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT] or is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP] or is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN] or is_key_pressed[pygame.K_s]:
                self.spaceship.decelerate()


    def _process_game_logic(self):
        """This function processes the game logic including moving objects, 
        collision detection, and scorekeeping"""
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        current_time = pygame.time.get_ticks()
        
        if self.message != "Game Over, score = " + str(globals.score):
            self.message = 'score = ' + str(globals.score) 

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "Game Over, score = " + str(globals.score) + ", You survived {str(globals.level)} rounds"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    globals.score += 100

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.asteroid_count += 1
            self.reset_game()
            print (self.asteroid_count)

    def _draw(self):
        """This function draws the game graphics on the screen"""
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(90)
        
    def _get_game_objects(self):
        """This function returns a list of all game objects"""
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects