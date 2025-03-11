import random

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound


def load_sprite(name, with_alpha=True):
    """Loads an image from the 'assets/sprites' folder. 
    Optionally keeps transparency information."""
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
 
    if with_alpha:
        return loaded_sprite.convert_alpha()  # Preserve alpha channel for transparency
    else:
        return loaded_sprite.convert()  # Convert image for faster blitting


def load_sound(name):
    """Loads a sound effect from the 'assets/sounds' folder."""
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position, surface):
    """Wraps a position around the edges of the game surface. 
    Useful for keeping objects on screen."""
    x, y = position
    width, height = surface.get_size()
    return Vector2(x % width, y % height)  # Modulo operation for wrapping


def get_random_position(surface):
    """Returns a random position within the bounds of the game surface."""
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    """Generates a random velocity vector with a magnitude between 
    min_speed and max_speed and a random direction."""
    speed = random.randint(min_speed, max_speed - 1)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)  # Create base vector and rotate


def print_text(surface, text, font, color=Color("white")):
    """Prints text onto the game surface using a provided font and color."""
    text_surface = font.render(text, False, color)

    rect = text_surface.get_rect()
    rect.center = (720, 100)  # Center the text at position (720, 100)

    surface.blit(text_surface, rect)  # Draw the text surface onto the main surface