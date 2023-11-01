import pygame
from .player import Player
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


class BasicAttack:
    def __init__(self, actor, damage, speed, image, direction):
        self.actor = actor
        self.damage = damage
        self.speed = speed
        self.image = image
        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.center = actor.rect.center

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x-10, self.rect.y))
        screen.blit(self.image, (self.rect.x+10, self.rect.y))


class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.Enemy_image = pygame.transform.rotate(pygame.transform.scale(load_image("../resources/assets/Battle/NPC.png"), (50, 50)),180)

        # Membuat objek Player
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)

        # Inisialisasi list untuk menyimpan basic attack karakter
        self.player_basic_attacks = []
        self.enemy_basic_attacks = []

        # Inisialisasi 3 Enemy dengan gambar yang telah Anda sediakan
        self.Enemys = []
        Enemy_x_positions = [400, 700, 1100]  # Atur posisi Enemy sesuai kebutuhan
        for x in Enemy_x_positions:
            Enemy = obj_Enemy(x, 50, self.Enemy_image, screen=self.screen)
            self.Enemys.append(Enemy)

    def run(self):
        current_time = pygame.time.get_ticks()
        
        # Gambar kembali objek pemain
        self.player.update()
        
        # Membuat dan mengupdate serangan dasar pemain
        for attack in self.player_basic_attacks:
            attack.update()
            attack.draw(self.screen)
        
        for attack in self.enemy_basic_attacks:
            attack.update()
            attack.draw(self.screen)
            
        # Menghapus serangan dasar yang melampaui batas
        self.player_basic_attacks = list(filter(lambda attack: attack.rect.y > 0, self.player_basic_attacks))
        self.enemy_basic_attacks = list(filter(lambda attack: attack.rect.y > 0, self.enemy_basic_attacks))
        
        # Membuat serangan dasar baru jika pemain menembak
        if len(self.Enemys) != 0:
            player_basic_attack = self.player.create_basic_attack_player(BasicAttack, self.player, len(self.player_basic_attacks), current_time, self.player.last_BasicAttack_time)
            if player_basic_attack is not None:
                self.player_basic_attacks.append(player_basic_attack)
                self.player.last_BasicAttack_time = current_time

            for enemy in self.Enemys:
                enemy_basic_attack = enemy.create_basic_attack_enemy(BasicAttack, enemy, len(self.enemy_basic_attacks), current_time, enemy.last_BasicAttack_time, cooldown_basicAttack=random.randint(2000,5000))
                if enemy_basic_attack is not None:
                    self.enemy_basic_attacks.append(enemy_basic_attack)
                    enemy.last_BasicAttack_time = current_time

        else:
            for attack in self.player_basic_attacks:
                if attack.rect.y <= 0:
                    self.player_basic_attacks.remove(attack)

            for attack in self.enemy_basic_attacks:
                if attack.rect.y >= self.screen_height:
                    self.enemy_basic_attacks.remove(attack)
        
        # Menggambar enemy
        for enemy in self.Enemys:
            enemy.draw(self.screen)
            enemy.draw_health()
            
            # Periksa tabrakan dengan serangan dasar
            for attack in self.player_basic_attacks:
                if enemy.health <= 0:
                    if enemy in self.Enemys : 
                        self.Enemys.remove(enemy)
                        self.player.score += 1
                if attack.rect.colliderect(enemy.rect):
                    enemy.health -= self.player.damage
                    self.player_basic_attacks.remove(attack)

            for enemy in self.Enemys:
                for attack in self.enemy_basic_attacks:
                    # Logika player kalah
                    
                    # if self.player.health <= 0:
                    #     ic("player kalah")
                    if attack.rect.colliderect(self.player.rect):
                        self.player.health -= enemy.damage
                        self.enemy_basic_attacks.remove(attack)
