from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sound, load_sprite, wrap_position
import globals
UP = Vector2(0, -1)


class GameObject:
    """This class represents a generic game object with a position, sprite, velocity, and radius for collision detection"""
    def __init__(self, position, sprite, velocity):
        """This function initializes the game object with the given position, sprite image, and velocity vector.
        Args:
            position (Vector2): The initial position of the game object.
            sprite (Surface): The pygame surface representing the image of the object.
            velocity (Vector2): The initial velocity vector of the object."""
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        """This function draws the game object onto the provided pygame surface.
        Args:
            surface (Surface): The pygame surface to draw the object on."""
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        """
        This function updates the position of the game object based on its velocity and wraps it around the screen edges.
        Args:
            surface (Surface): The pygame surface representing the game screen."""
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        """This function checks for collision between this game object and another game object using their positions and radii.
        Args:
            other_obj (GameObject): The other game object to check for collision with.
        Returns:
            bool: True if there is a collision, False otherwise."""
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    """This class represents the spaceship game object"""
    MANEUVERABILITY = 3
    ACCELERATION = 0.1
    BULLET_SPEED = 3 + globals.score_multiplier
    DECELERATION = ACCELERATION * -1
    def __init__(self, position, create_bullet_callback):
        """This function initializes the spaceship object with the given position and a callback function to create new bullets.
        Args:
            position (Vector2): The initial position of the spaceship.
            create_bullet_callback (function): A function that takes a Bullet object as an argument and adds it to the game."""
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        """This function rotates the spaceship clockwise or counter-clockwise based on the argument.
        Args:
            clockwise (bool, optional): True to rotate clockwise, False to rotate counter-clockwise. Defaults to True."""
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        """This function accelerates the spaceship in the direction it's facing"""
        self.velocity += self.direction * self.ACCELERATION
        if self.velocity == 0 and globals.level <=3:
            self.velocity += 1
    def decelerate(self):
        """This function decelerates the spaceship in the direction it's facing"""
        self.velocity += self.direction * self.DECELERATION

    def draw(self, surface):
        """This function draws the spaceship onto the provided pygame surface with a rotation based on its direction.
    Args:
        surface (Surface): The pygame surface to draw the object on."""
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        '''This function fires a bullet from the spaceship and plays a laser sound effect.'''
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

class Asteroid(GameObject):
    """This class represents an asteroid game object"""
    def __init__(self, position, create_asteroid_callback, size=3):
        """This function initializes the asteroid object with the given position, a callback function to create new asteroids, and a size (defaulting to 3).
        Args:
            position (Vector2): The initial position of the asteroid. create_asteroid_callback (function): A function that takes an Asteroid object as an argument and adds it to the game.
            size (int, optional): The size of the asteroid (3, 2, or 1). Defaults to 3."""
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        '''This function splits a large asteroid into two smaller asteroids upon collision.'''
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    """This class represents a bullet game object"""
    def __init__(self, position, velocity):
        """This function initializes the bullet object with the given position and velocity.
        Args:
            position (Vector2): The initial position of the bullet.
            velocity (Vector2): The initial velocity vector of the bullet."""
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        """This function updates the position of the bullet based on its velocity 
        and removes it if it goes off-screen.
        Args:
            surface (Surface): The pygame surface representing the game screen."""
        self.position = self.position + self.velocity