import pygame
pygame.font.init()

score = 0
level = 1
score_multiplier = float(score) / 200
WIDTH = 1440
HEIGHT = 900
buzzer_count = 0
buzzer_max = 3
font = pygame.font.Font(None, 24)
asteroid_number = 6
game = True