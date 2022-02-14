from asteroid import *
import pygame
from constants import *

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    screen.fill((0, 0, 0))

    asteroid = Asteroid(screen, position, (255, 0, 0), LARGE_ASTEROID,
                        random.choice(init_dx), random.choice(init_dy), 0.25)
    asteroids = [asteroid]

    running = True
    while running:
        for a in asteroids:
            a.move_asteroid()
            a.draw_asteroid()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.type == pygame.QUIT:
                    running = False
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_1:
                    asteroid.size = LITTLE_ASTEROID
                if event.key == K_2:
                    asteroid.size = NORMAL_ASTEROID
                if event.key == K_3:
                    asteroid.size = LARGE_ASTEROID

                # Change direction just for mechanics testing
                if event.key == K_RIGHT:
                    asteroid.dx = 'RIGHT'
                if event.key == K_LEFT:
                    asteroid.dx = 'LEFT'
                if event.key == K_UP:
                    asteroid.dy = 'UP'
                if event.key == K_DOWN:
                    asteroid.dy = 'DOWN'

                # Change asteroid speed for mechanics testing
                if event.key == K_BACKSPACE:
                    asteroid.speed = 0.125
                if event.key == K_SPACE:
                    asteroid.speed = 0.5

                # Split the asteroid
                if event.key == K_s:
                    newbies = []

                    for a in asteroids:
                        if res := a.split_asteroid():
                            newbies += res

                    asteroids = list(newbies)

        screen.fill((0, 0, 0))

pygame.quit()
