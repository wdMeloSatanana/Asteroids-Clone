import random
import time
import pygame
from pygame.image import load

from constants import *
from asteroid import Asteroid
from player import Spaceship
from pygame.constants import *


# from ufo import UFO


class Screen:
    def __init__(self):
        self.score = 0
        self._init_pygame()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = load(f"assets/sprites/space.png")
        self.clock = pygame.time.Clock()
        self.asteroid_sprite = load(f"assets/sprites/asteroid.png")
        self.asteroids = [
            Asteroid(self.screen, random.choice(position), self.asteroid_sprite, random.choice(sizes),
                     random.choice(init_dx), random.choice(init_dy), 0.25),
            Asteroid(self.screen, random.choice(position), self.asteroid_sprite, random.choice(sizes),
                     random.choice(init_dx), random.choice(init_dy), 0.25),
            Asteroid(self.screen, random.choice(position), self.asteroid_sprite, random.choice(sizes),
                     random.choice(init_dx), random.choice(init_dy), 0.25),
            Asteroid(self.screen, random.choice(position), self.asteroid_sprite, random.choice(sizes),
                     random.choice(init_dx), random.choice(init_dy), 0.25)
        ]
        'self.ufo = UFO()'
        self.spaceship = Spaceship((400, 300), 3)
        self.wave = 1

    def main_loop(self):
        while True:
            self._handle_input()
            self.draw_hud()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.spaceship.shoot(self.screen)
                 
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                quit()

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.spaceship.accelerate()
        if is_key_pressed[pygame.K_DOWN]:
            self.spaceship.slow_down()
        

    def _process_game_logic(self):
        self.spaceship.move(self.screen)

    def show_lives(self, surface):

        self.surface = surface
        font = pygame.font.SysFont('times new roman', 30)
        text = font.render('Lives: ' + str(self.spaceship.lives), False, (255, 0 , 0))
        text_rect = text.get_rect()
        text_rect.center = (50, 15)
        self.surface.blit(text, text_rect)

        text = font.render('Points: ' + str(self.score), False, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (70, 50)
        self.surface.blit(text, text_rect)
        

    def show_waves(self):
        font = pygame.font.SysFont('times new roman', 60)
        text = font.render('Wave ' + str(self.wave), False, (0, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (400, 300)
        self.screen.blit(text, text_rect)
        pygame.display.update()
        time.sleep(3)

    def draw_hud(self):

        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        self.spaceship.move(self.screen)
        screen.show_lives(self.screen)

        for bullet in self.spaceship.bullets:
            bullet.draw()
            is_valid_position = bullet.move()
            if not is_valid_position:
                self.spaceship.bullets.remove(bullet)
                
        for asteroid in self.asteroids:
            asteroid.draw_asteroid()
            asteroid.move_asteroid()

        self.collision()

        pygame.display.flip()
        self.clock.tick(60)

    def collision(self):
        new_asteroids = []

        for asteroid in self.asteroids:
            if asteroid.collided_with(self.spaceship.position):
                self.spaceship.lives -= 1
                screen.restart()
            for bullet in self.spaceship.bullets:
                if asteroid.collided_with(bullet.position):
                    self.score += 100
                    if res := asteroid.split_asteroid():
                        new_asteroids += res
                    self.spaceship.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

        if new_asteroids:
            self.asteroids += new_asteroids
        
        if len(self.asteroids) == 0:
            self.wave += 1
            screen.show_waves()
            screen.restart()
            
    def restart(self):

        if self.spaceship.lives > 0:
            self.asteroids = []
            for i in range(4 + (self.wave - 1)):
                self.asteroids.append(Asteroid(self.screen, random.choice(position), self.asteroid_sprite, random.choice(sizes),
                     random.choice(init_dx), random.choice(init_dy), 0.25))
            self.asteroids.append(Asteroid(self.screen, random.choice(position), self.asteroid_sprite, LARGE_ASTEROID,
                     random.choice(init_dx), random.choice(init_dy), 0.25))
            'self.ufo = UFO()'
            self.spaceship = Spaceship((400, 300), self.spaceship.lives)

        else:
            font = pygame.font.SysFont('times new roman', 60)
            text = font.render('Game Over', False, (0, 255, 0))
            text_rect = text.get_rect()
            text_rect.center = (400, 300)
            self.screen.blit(text, text_rect)
            pygame.display.update()
            time.sleep(3)
            quit()


if __name__ == "__main__":
    screen = Screen()
    screen.main_loop()
