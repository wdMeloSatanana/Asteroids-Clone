import pygame
from pygame.math import Vector2


class Bullet:

    def __init__(self, surface, position, direction):
        self.surface = surface
        self.position = position
        self.direction = Vector2(direction[0], direction[1])

    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 0), self.position, 5)

    def move(self):
        self.position = self.position + self.direction.normalize() * 5

        if self.position[0] > 800 or self.position[0] < 0:  # Crossing horizontally
            print(self.position)
            return False
        if self.position[1] > 600 or self.position[1] < 0:  # Crossing vertically
            print(self.position)
            return False

        return True

