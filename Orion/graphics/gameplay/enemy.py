import pygame
import random
import os

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar
    
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, health, damage, speed, screen_width, screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.health = health
        self.damage = damage
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self):
        pass

    def update(self):
        pass

class KamikazeEnemy(Enemy):
    def __init__(self, screen_width, screen_height):
        image = pygame.transform.scale(load_image("../resources/assets/Battle/NPC.png"), (70, 70))
        super().__init__(image, health=10, damage=5, speed=8, screen_width=screen_width, screen_height=screen_height)

    def move(self):
        # Implementasi pergerakan kamikaze enemy
        pass

    def update(self):
        # Implementasi pembaruan kamikaze enemy
        pass

class ShooterEnemy(Enemy):
    def __init__(self, screen_width, screen_height, x, y,):
        image = pygame.transform.scale(load_image("../resources/assets/Battle/NPC.png"), (70, 70))
        super().__init__(image, health=20, damage=10, speed=5, screen_width=screen_width, screen_height=screen_height)
        self.basic_attack_path = load_image("../resources/assets/Battle/bullet.png")
        self.x = x
        self.y = y
        self.basic_attack_cooldown = 500
        self.last_basicAttack_time = 0
        self.rect = self.image.get_rect()

    def move(self, lvl=None, speed=2):
        self.rect.y += self.speed

    def update(self):
        self.move()


    def create_basic_attack_enemy(self, BasicAttack, player, amount_BasicAttack, current_time, last_time):
        last_time = 0  # Atur nilai awal yang sesuai untuk last_time
        if amount_BasicAttack <= 4 and current_time - last_time >= 30:
            return BasicAttack(player, damage=10, speed=20, image=pygame.transform.scale(self.basic_attack_path, (30, 30)), direction="down")
        return None


class StageBoss(Enemy):
    def __init__(self, screen_width, screen_height):
        image = pygame.transform.scale(load_image("../resources/assets/Battle/BOSS.png"), (70, 70))
        super().__init__(image, health=100, damage=15, speed=3, screen_width=screen_width, screen_height=screen_height)

    def move(self):
        # Implementasi pergerakan bos tahap
        pass

    def update(self):
        # Implementasi pembaruan bos tahap
        pass

class MainBoss(Enemy):
    def __init__(self, screen_width, screen_height):
        image = pygame.transform.scale(load_image("../resources/assets/Battle/BOSS.png"), (70, 70))
        super().__init__(image, health=500, damage=25, speed=2, screen_width=screen_width, screen_height=screen_height)

    def move(self):
        # Implementasi pergerakan bos utama
        pass

    def update(self):
        # Implementasi pembaruan bos utama
        pass
