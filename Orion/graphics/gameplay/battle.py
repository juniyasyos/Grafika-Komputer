import pygame
from .player import Player
from icecream import ic
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

class Target:
    def __init__(self, x, y, image, screen):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.health = 150
        self.max_health = 150

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def draw_health(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, current_health_width, 5))


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
        screen.blit(self.image, self.rect)


class skill:
    def __init__(self, actor, damage, speed, image) -> None:
        self.actor = actor
        self.damage = damage
        self.speed = speed
        self.image = image

    # def update(self):
    #     self.actor.s


class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.target_image = pygame.transform.scale(load_image("../resources/assets/Battle/target.png"),(50,50))

        # Membuat objek Player
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        
        # Inisialisasi list untuk menyimpan basic attack
        self.player_basic_attacks = []

        # Inisialisasi 3 target dengan gambar yang telah Anda sediakan
        self.targets = []
        target_x_positions = [400, 700, 1100]  # Atur posisi target sesuai kebutuhan
        for x in target_x_positions:
            target = Target(x, 50, self.target_image, screen=self.screen)
            self.targets.append(target)

    def run(self):
        current_time = pygame.time.get_ticks()
        
        # Gambar kembali objek pemain
        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Menggambar dan mengupdate serangan dasar
        if self.targets != []:
            # Basic attack Player
            player_basicAttack = self.player.create_basic_attack_player(BasicAttack=BasicAttack, player=self.player, current_time=current_time, last_time=self.player.last_BasicAttack_time, amount_BasicAttack=len(self.player_basic_attacks))
            if player_basicAttack is not None:
                self.player_basic_attacks.append(player_basicAttack)
                self.player.last_BasicAttack_time = current_time

            for attack in self.player_basic_attacks:
                attack.update()
                attack.draw(self.screen)

                # Periksa tabrakan dengan target
                for target in self.targets:
                    if target.health <= 0:
                        self.targets.remove(target)
                        self.player.score+=1

                    if attack.rect.colliderect(target.rect):
                        # ic(attack.rect.colliderect(target.rect))
                        # ic(target.health)
                        target.health-=self.player.get_damage()
                        self.player_basic_attacks.remove(attack)
        
        else:
            for attack in self.player_basic_attacks:
                attack.update()
                attack.draw(self.screen)
                
                if attack.rect.y <= 0:
                    self.player_basic_attacks.remove(attack)
        
        # hapus basic attack jika melampui batas
        for attack in self.player_basic_attacks:                
            if attack.rect.y <= 0:
                self.player_basic_attacks.remove(attack)

        # Menggambar target
        for target in self.targets:
            target.draw(self.screen)
            target.draw_health()

        # Draw player health bar and score
        self.player.draw_health_bar(self.screen)
        self.player.draw_score(self.screen)