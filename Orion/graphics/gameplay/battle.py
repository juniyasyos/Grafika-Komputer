import pygame
from .player import Player
from .enemy import obj_Enemy, EnemyType1
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

class Attact_Actor (pygame.sprite.Sprite):
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

    def draw(self, screen, func=None):
        if func is not None:
            pass
        screen.blit(self.image, (self.rect.x-10, self.rect.y))
        screen.blit(self.image, (self.rect.x+10, self.rect.y))


class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.Enemy_image = pygame.transform.rotate(pygame.transform.scale(load_image("../resources/assets/Battle/NPC.png"), (50, 50)), 180)
        self.start_game = pygame.time.get_ticks()

        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        self.player_basic_attacks = pygame.sprite.Group()
        self.player_rocket = pygame.sprite.Group()

        # Membuat objek Enemy dan elemennya
        self.Enemys = []
        self.enemy_basic_attacks = pygame.sprite.Group()

    def run_battle(self):
        self.current_time = pygame.time.get_ticks()
        self.player.update()                        # Gambar kembali objek pemain
        self.attack_player()                        # Update attack player
        self.attack_enemy()                         # Update attack enemy
        self.remove_elemen_obj()                    # Menghapus object yang melebihi layar
        self.cek_basic_attack()                     # Cek object yang melebihi layar
        self.create_enemy()

    def attack_player(self):
        for attack in self.player_basic_attacks:
            attack.update()
            attack.draw(self.screen)
    
    def attack_enemy(self):
        for attack in self.enemy_basic_attacks:
            attack.update()
            attack.draw(self.screen)
        
    def remove_elemen_obj(self):
        # Menghapus serangan dasar yang melampaui batas
        self.player_basic_attacks = list(filter(lambda attack: attack.rect.y > 0, self.player_basic_attacks))
        self.enemy_basic_attacks = list(filter(lambda attack: attack.rect.y < self.screen_height, self.enemy_basic_attacks))
    
    def cek_basic_attack(self):
        for enemy in self.Enemys:
            enemy_basic_attack = enemy.create_basic_attack_enemy(Attact_Actor, enemy, len(self.enemy_basic_attacks), self.current_time, enemy.last_BasicAttack_time, cooldown_basicAttack=random.randint(2000, 5000))
            if enemy_basic_attack is not None:
                self.enemy_basic_attacks.append(enemy_basic_attack)
                enemy.last_BasicAttack_time = self.current_time

        if self.Enemys:
            player_basic_attack = self.player.create_basic_attack_player(Attact_Actor, self.player, len(self.player_basic_attacks), self.player.last_BasicAttack_time)
            if player_basic_attack is not None:
                self.player_basic_attacks.append(player_basic_attack)
                self.player.last_BasicAttack_time = self.current_time

    def create_enemy(self):
        for enemy in self.Enemys:
            if self.current_time - self.start_game >= enemy.delay_to_next_path[0]:
                enemy.draw(self.screen)
                enemy.draw_health()
                enemy_attack = False

                for attack in self.player_basic_attacks:
                    if enemy.health <= 0:
                        if enemy in self.Enemys: 
                            self.Enemys.remove(enemy)
                            self.player.score += 1
                    if attack.rect.colliderect(enemy.rect):
                        enemy.health -= self.player.damage
                        self.player_basic_attacks.remove(attack)

            for enemy in self.Enemys:
                for attack in self.enemy_basic_attacks:
                    if attack.rect.colliderect(self.player.rect):
                        self.player.take_damage(self.player.damage)
                        self.enemy_basic_attacks.remove(attack)
                    
                remove_enemy = enemy.update()
                if remove_enemy is True or enemy.path_index >= len(enemy.path):
                    self.Enemys.remove(enemy)



class level_1(Battle):
    def __init__(self, screen, screen_height, screen_width):
        super().__init__(screen, screen_height, screen_width)
        self.stage_index = 0
        self.stage_delay =  pygame.time.get_ticks()
        self.stage = {
            "Stage 1" : [
                EnemyType1(screen=self.screen,path=[(100, 100), (300, 50), (self.player.rect.x, self.player.rect.y)], delay=[0, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 50), (450, 100), (self.screen_width, 100)], delay=[200, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (550, 50), (self.screen_width, 200)], delay=[300, 3000, 0]),
                ],
            "Stage 2" : [
                EnemyType1(screen=self.screen,path=[(300, 50), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[0, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 50), (500, 50), (self.screen_width, 100)], delay=[200, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[300, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[400, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[500, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (90, 50), (self.screen_width, 200)], delay=[600, 3000, 0])
                ],
            "Stage 3" : [
                EnemyType1(screen=self.screen,path=[(0, 0), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[100, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (500, 50), (self.screen_width, 100)], delay=[200, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[300, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[400, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[500, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (900, 50), (self.screen_width, 200)], delay=[600, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (1000, 50), (self.screen_width, 200)], delay=[700, 3000, 0]),
                EnemyType1(screen=self.screen,path=[(0, 0), (1100, 50), (self.screen_width, 200)], delay=[800, 3000, 0])
                ],
            "delay":[0, 12000, 10000]
            }
    
    def run(self):
        if len(self.Enemys) == 0:
            if self.stage_index+1 < len(self.stage):
                if pygame.time.get_ticks() - self.stage_delay >= self.stage["delay"][self.stage_index]:
                    self.stage_index += 1
                    self.Enemys = self.stage[f"Stage {self.stage_index}"]
                    self.stage_delay = pygame.time.get_ticks()
        self.run_battle()
