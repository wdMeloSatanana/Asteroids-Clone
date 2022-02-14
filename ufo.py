import pygame
from bullet import Bullet


class UFO:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    class ufo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.dir_choice = ()
        self.bullets = []
        self.cd = 0
        self.b_dir = 0
        self.dir = 0
        self.size = 0

    def update_ufo(self):
        # Move player
        self.x += ALIEN_SPEED * math.cos(self.dir * math.pi / 180)
        self.y += ALIEN_SPEED * math.sin(self.dir * math.pi / 180)

        # Choose random direction
        if random.randrange(0, 100) == 1:
            self.dir = random.choice(self.dir_choice)
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
        if self.x < 0 or self.x > WIDTH:
            self.state = "Dead"

        # Shooting
        if self.type == "Large":
            self.b_dir = random.randint(0, 360)
        if self.cd == 0:
            self.bullets.append(Bullet(self.x, self.y, self.b_dir))
            self.cd = 30
        else:
            self.cd -= 1


    def create_ufo(self):
        # Create saucer
        # Set state
        self.state = "Alive"

        # Set random position
        self.x = random.choice((0, WIDTH))
        self.y = random.randint(0, HEIGHT)

        # Set random type
        if random.randint(0, 1) == 0:
            self.type = "Large"
            self.size = 20
        else:
            self.type = "Small"
            self.size = 10

        # Create random direction
        if self.x == 0:
            self.dir = 0
            self.dir_choice = (0, 45, -45)
        else:
            self.dir = 180
            self.dir_choice = (180, 135, -135)

        # Reset bullet wait time
        self.cd = 0

    def draw_ufo(self):
        # Draw saucer
        pygame.draw.polygon(gameDisplay, WHITE,
                            ((self.x + self.size, self.y),
                             (self.x + self.size / 2, self.y + self.size / 3),
                             (self.x - self.size / 2, self.y + self.size / 3),
                             (self.x - self.size, self.y),
                             (self.x - self.size / 2, self.y - self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)
        pygame.draw.line(gameDisplay, WHITE,
                         (self.x - self.size, self.y),
                         (self.x + self.size, self.y))
        pygame.draw.polygon(gameDisplay, WHITE,
                            ((self.x - self.size / 2, self.y - self.size / 3),
                             (self.x - self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)
