import pygame
from icecream import ic
import os
import random
import math
from .. import gameplay as gp
        
class obj_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, screen, path, delay):
        super().__init__()
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
        self.start_time = 0
        self.last_time = pygame.time.get_ticks()
        self.path = path
        self.delay_to_next_path = delay
        self.path_index = 0
        self.delay_start_time = 0
        self.speed = 10
        self.basic_attack_speed = 10
        self.basic_attack_image = gp.load_image(image_filename="../resources/assets/Battle/bullet.png", rotation=180, colorkey=(255,255,255),size=(16,24), scale=2)
        self.set_update_enemy = []

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update_basic(self):
        if pygame.time.get_ticks() - self.last_time >= self.delay_to_next_path[0]:
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
    

class EnemyType1(obj_Enemy):
    def __init__(self, screen, path, delay, x=0, y=0):
        image = gp.load_image("../resources/assets/Battle/NPC.png",size=(50,50), rotation=180, colorkey=(255,255,255))
        super().__init__(x, y, image, screen, path, delay)
        self.enemy_basic_attacks = pygame.sprite.Group()
        self.health = 300
        self.max_health = 300
        self.basic_attack_speed = 6

    def create_basic_attack_enemy(self, BasicAttack, enemy, current_time, last_time, cooldown_basicAttack, count_all_enemy):
        if pygame.time.get_ticks() - self.last_time > self.delay_to_next_path[0]+2000:
            if current_time - last_time >= cooldown_basicAttack:
                self.enemy_basic_attacks.add(
                    BasicAttack(
                        screen=self.screen,
                        actor=enemy, 
                        speed=self.basic_attack_speed,
                        image=self.basic_attack_image, 
                        attack_type="Spesial"
                        )
                    )
                self.last_BasicAttack_time = gp.pygame.time.get_ticks()
    
    def set_basicAttack_func(self):
        for attack in self.enemy_basic_attacks.sprites():
            attack.rect.y += attack.speed
            self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))
            
    def update(self):
        self.update_basic()
        self.set_basicAttack_func()

        