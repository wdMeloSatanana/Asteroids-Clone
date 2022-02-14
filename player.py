from pygame.math import Vector2
from pygame.transform import rotozoom
from pygame.image import load
from bullet import *


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
    loaded_sprite = pygame.transform.scale(loaded_sprite, (50,50))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        self.sprite_rect = self.sprite.get_rect(center=self.position)
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, self.sprite_rect)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25

    def __init__(self, position, lives):
        # Make a copy of the original UP vector
        self.score = 0
        self.lives = lives
        self.direction = Vector2(UP)
        self.bullets = []

        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def slow_down(self):
        self.velocity -= self.direction * self.ACCELERATION

    def shoot(self, surface):
        if len(self.bullets) < 4:
            a = self.bullets.append(
                Bullet(surface, self.position, self.direction)
            )
