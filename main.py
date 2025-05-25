import pygame
import math
from sys import exit

pygame.init()

WIDTH, HEIGHT = 800, 800

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.color = (255, 255, 255)
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.jumping = False
        self.acceleration = 0.5
        self.deceleration = 0.2
        self.max_speed = 5.0
        self.jump_strength = -10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.horizontal_speed = max(self.horizontal_speed - self.acceleration, -self.max_speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.horizontal_speed = min(self.horizontal_speed + self.acceleration, self.max_speed)
        else:
            if self.horizontal_speed > 0:
                self.horizontal_speed = max(0, self.horizontal_speed - self.deceleration)
            elif self.horizontal_speed < 0:
                self.horizontal_speed = min(0, self.horizontal_speed + self.deceleration)

        if keys[pygame.K_SPACE] and not self.jumping:
            self.vertical_speed = self.jump_strength
            self.jumping = True

        self.vertical_speed += 0.5

        self.x += self.horizontal_speed
        self.y += self.vertical_speed

        if self.x < -self.width:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = -self.width

        self.rect.topleft = (self.x, self.y)

        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vertical_speed = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Cannon:
    def __init__(self, player):
        self.player = player
        self.original_image = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (0, 255, 0), (0, 0, 50, 20))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.num_rays = 36
        self.ray_angles = list(range(-15, 16, 1))

    def point_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

    def cast_ray(self, target):
        cannon_center = self.player.rect.center
        ray_length = 1600

        for angle in self.ray_angles:
            dx = math.cos(math.radians(self.angle + angle))
            dy = math.sin(math.radians(self.angle + angle))

            hit_target = False
            hit_point = None
            for step in range(ray_length):
                x = int(cannon_center[0] + dx * step)
                y = int(cannon_center[1] + dy * step)

                if not 0 <= x < WIDTH or not 0 <= y < HEIGHT:
                    break

                if target.rect.collidepoint(x, y):
                    hit_target = True
                    hit_point = (x, y)
                    break

            if hit_target:
                pygame.draw.line(screen, (255, 0, 0), cannon_center, hit_point, 2)
                pygame.draw.circle(screen, (255, 255, 255), hit_point, 4)
            else:
                hit_point = (int(cannon_center[0] + dx * ray_length), int(cannon_center[1] + dy * ray_length))
                pygame.draw.line(screen, (255, 0, 0), cannon_center, hit_point, 2)


class Target:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

player = Player(WIDTH // 2, HEIGHT - 200)
cannon = Cannon(player)
targets = [Target(200, 400, 50), Target(400, 400, 50), Target(600, 400, 50)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60)
    dt /= 1000.0

    player.move(dt)

    screen.fill((0, 0, 0))
    player.draw(screen)
    cannon.point_to_mouse()
    
    for target in targets:
        cannon.cast_ray(target)
        target.draw(screen)

    pygame.display.flip()

pygame.quit()
exit()
