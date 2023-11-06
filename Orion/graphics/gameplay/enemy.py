import pygame
from icecream import ic
import os
import random
import math

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e
        
class obj_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, screen, path, delay):
        super().__init__()
        self.x = 0
        self.y = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.health = 150
        self.max_health = 150
        self.last_BasicAttack_time = 0
        self.damage = 50
        self.start_time = 0
        self.last_time = pygame.time.get_ticks()
        self.path = path
        self.delay_to_next_path = delay
        self.path_index = 0
        self.delay_start_time = 0
        self.speed = 5
        self.basic_attack_path = pygame.transform.rotate(load_image("../resources/assets/Battle/bullet.png"), 180)
        self.set_update_enemy = []

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        if pygame.time.get_ticks() - self.last_time >= self.delay_to_next_path[0]:
            for func_update_enemy in self.set_update_enemy: func_update_enemy()

            if self.path_index < len(self.path):
                target_x, target_y = self.path[self.path_index]
                dx = target_x - self.x
                dy = target_y - self.y

                distance = dx * dx + dy * dy

                tolerance_squared = 10
                if distance < tolerance_squared:
                    if pygame.time.get_ticks() - self.delay_start_time > self.delay_to_next_path[self.path_index]:
                        self.path_index += 1
                        self.delay_start_time = pygame.time.get_ticks()
                else:
                    self.move_towards(target_x, target_y, self.speed)
            return False
        else:
            return False
        return True

    def move_towards(self, target_x, target_y, speed):
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        
        if distance != 0:
            delta_x /= distance
            delta_y /= distance
        
        move_x = delta_x * speed
        move_y = delta_y * speed

        self.x += move_x
        self.y += move_y
        self.rect.topleft = (int(self.x), int(self.y))
    
    def draw_health(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y + 90, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y + 90, current_health_width, 5))
    
    def create_basic_attack_enemy(self, BasicAttack, enemy, amount_BasicAttack, current_time, last_time, cooldown_basicAttack):
        if pygame.time.get_ticks() - self.last_time >= self.delay_to_next_path[0]:
            if current_time - last_time >= cooldown_basicAttack:
                return BasicAttack(enemy, damage=10, speed=15, image=pygame.transform.scale(self.basic_attack_path, (30, 30)), direction="down")
        return None

class EnemyType1(obj_Enemy):
    def __init__(self, screen, path, delay, x=0, y=0):
        image = pygame.transform.rotate(pygame.transform.scale(load_image("../resources/assets/Battle/NPC.png"), (70, 70)), 180)
        super().__init__(x, y, image, screen, path, delay)