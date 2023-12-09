import pygame
import sys
import random
import math

# Inisialisasi Pygame
pygame.init()

# Pengaturan layar
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Balls")

# Warna
white = (255, 255, 255)

# Kelas Bola
class Ball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.randint(2, 4)
        self.angle = angle

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Inisialisasi bola
num_balls = 50
start_angle = random.uniform(0, 2 * math.pi)
angle_increment = 2 * math.pi / num_balls
balls = [Ball(width // 2, height // 2, start_angle + i * angle_increment) for i in range(num_balls)]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Perbarui posisi bola dan gambar
    for ball in balls:
        ball.move()

    # Bersihkan layar
    screen.fill(white)

    # Gambar bola
    for ball in balls:
        ball.draw()

    # Perbarui tampilan
    pygame.display.flip()

    # Batasi kecepatan frame
    pygame.time.Clock().tick(60)
