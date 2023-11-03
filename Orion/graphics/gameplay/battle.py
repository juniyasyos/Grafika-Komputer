import pygame
from .player import Player
from .enemy import obj_Enemy
from icecream import ic
import os
import random
import threading

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e

class BasicAttack(pygame.sprite.Sprite):
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

        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        self.player_basic_attacks = pygame.sprite.Group()

        # Membuat objek Enemy dan elemennya
        self.Enemys = [obj_Enemy(random.randint(100,800), 50, self.Enemy_image, screen=self.screen)]
        self.enemy_basic_attacks = pygame.sprite.Group()

    def run(self):
        current_time = pygame.time.get_ticks()
        
        # Gambar kembali objek pemain
        update_player = lambda: self.player.update()
        
        def thread_attack_player():
            # Membuat dan mengupdate serangan dasar pemain
            for attack in self.player_basic_attacks:
                attack.update()
                attack.draw(self.screen)
        
        def thread_attack_enemy():
            for attack in self.enemy_basic_attacks:
                attack.update()
                attack.draw(self.screen)
            
        def remove_elemen_obj():
            # Menghapus serangan dasar yang melampaui batas
            self.player_basic_attacks = list(filter(lambda attack: attack.rect.y > 0, self.player_basic_attacks))
            self.enemy_basic_attacks = list(filter(lambda attack: attack.rect.y < self.screen_height, self.enemy_basic_attacks))
        
        def cek_basic_attack():
            # Membuat serangan dasar baru jika pemain menembak
            for enemy in self.Enemys:
                enemy_basic_attack = enemy.create_basic_attack_enemy(BasicAttack, enemy, len(self.enemy_basic_attacks), current_time, enemy.last_BasicAttack_time, cooldown_basicAttack=random.randint(2000,5000))
                if enemy_basic_attack is not None:
                    self.enemy_basic_attacks.append(enemy_basic_attack)
                    enemy.last_BasicAttack_time = current_time

            if self.Enemys:
                player_basic_attack = self.player.create_basic_attack_player(BasicAttack, self.player, len(self.player_basic_attacks), current_time, self.player.last_BasicAttack_time)
                if player_basic_attack is not None:
                    self.player_basic_attacks.append(player_basic_attack)
                    self.player.last_BasicAttack_time = current_time
        
        def create_enemy():
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

        
        threads = []
        for operation in [thread_attack_player, thread_attack_player, remove_elemen_obj, update_player, cek_basic_attack, create_enemy]:
            thread = threading.Thread(target=operation)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()