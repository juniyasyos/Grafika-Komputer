import pygame
from icecream import ic
import os
import random

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e
        
class obj_Enemy:
    def __init__(self, x, y, image, screen):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.health = 150
        self.max_health = 150
        self.last_BasicAttack_time = 0
        self.damage = 50
        self.basic_attack_path = pygame.transform.rotate(load_image("../resources/assets/Battle/bullet.png"), 180)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def draw_health(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, current_health_width, 5))
    
    def create_basic_attack_enemy(self, BasicAttack, enemy, amount_BasicAttack, current_time, last_time, cooldown_basicAttack):
        if current_time - last_time >= cooldown_basicAttack:
            return BasicAttack(enemy, damage=10, speed=15, image=pygame.transform.scale(self.basic_attack_path, (30, 30)), direction="down")
        return None