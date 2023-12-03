import pygame
import sys
import math
import os

class GameObject:
    def __init__(self, image_filename, size=(16, 9), rotation=None, colorkey=None, scale=None):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, image_filename)

        try:
            self.original_image = pygame.image.load(image_path)
            self.original_image = pygame.transform.scale(self.original_image, size)

            if colorkey is not None:
                self.original_image.set_colorkey(colorkey)

            if rotation is not None:
                self.original_image = pygame.transform.rotate(self.original_image, rotation)

            if scale is not None:
                self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale),
                                                                                  int(self.original_image.get_height() * scale)))

            self.image = self.original_image.convert_alpha()
            self.rect = self.image.get_rect()
        except pygame.error as e:
            print(f"Failed to load image: {image_filename}")
            raise e

class Player(GameObject):
    def __init__(self, image_filename, size=(16, 9), rotation=None, colorkey=None, scale=None):
        super().__init__(image_filename, size, rotation, colorkey, scale)
        self.speed = 5

    def move(self, keys):
        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

    def rotate_towards_target(self):
        target_x, target_y = pygame.mouse.get_pos()
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        angle = math.atan2(dy, dx)
        angle_deg = math.degrees(angle)
        return pygame.transform.rotate(self.image, -angle_deg-90)

pygame.init()

width, height = 600, 400
white = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kotak Mengikuti Mouse dengan Gambar")

box_size = 50
target_size = 30
target_color = (255, 0, 0)

player = Player("graphics/resources/assets/Battle/PLAYER.png", size=(box_size, box_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.move(keys)

    screen.fill(white)

    rotated_box = player.rotate_towards_target()
    screen.blit(rotated_box, player.rect.topleft)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
