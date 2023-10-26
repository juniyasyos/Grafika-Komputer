import pygame
from .player import Player
from icecream import ic
import os

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

class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.last_attack_time = 0
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.target_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory,"../resources/assets/target.png")).convert_alpha(), (50, 50))

        # Membuat objek Player
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        self.asset_basicAttack_Player = self.player.basic_attack_path

        # Inisialisasi list untuk menyimpan serangan dasar
        self.basic_attacks = []

        # Inisialisasi 3 target dengan gambar yang telah Anda sediakan
        self.targets = []
        target_x_positions = [400, 700, 1100]  # Atur posisi target sesuai kebutuhan
        for x in target_x_positions:
            target = Target(x, 50, self.target_image, screen=self.screen)
            self.targets.append(target)

    def run(self):
        current_time = pygame.time.get_ticks()

        # Cek apakah sudah waktunya untuk serangan dasar baru
        if current_time - self.last_attack_time >= 500:
            self.create_basic_attack_player()  # Membuat serangan dasar baru
            self.last_attack_time = current_time  # Perbarui waktu serangan terakhir

        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Gambar kembali objek pemain
        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Menggambar dan mengupdate serangan dasar
        if self.targets != []:
            for attack in self.basic_attacks:
                attack.update()
                attack.draw(self.screen)

                # Periksa tabrakan dengan target
                for target in self.targets:
                    if target.health <= 0:
                        self.targets.remove(target)
                        self.player.score+=1
                    if attack.rect.colliderect(target.rect):
                        ic(attack.rect.colliderect(target.rect))
                        ic(target.health)
                        target.health-=self.player.get_damage()
                        self.basic_attacks.remove(attack)

        # Menggambar target
        for target in self.targets:
            target.draw(self.screen)
            target.draw_health()

        # Draw player health bar and score
        self.player.draw_health_bar(self.screen)
        self.player.draw_score(self.screen)

        # Draw countdown cooldown text
        cooldown_text = self.player.font.render(self.player.skill_cooldown_text, True, (255, 255, 255))
        self.screen.blit(cooldown_text, (10, 10))

    def create_basic_attack_player(self):
        # Membuat serangan dasar baru dan menambahkannya ke daftar serangan dasar
        basic_attack = BasicAttack(self.player, damage=10, speed=20, image=pygame.transform.scale((pygame.image.load(self.asset_basicAttack_Player)),(50,50)), direction="up")
        self.basic_attacks.append(basic_attack)