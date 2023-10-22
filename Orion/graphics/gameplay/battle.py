import pygame
from .player import Player
from icecream import ic

class Target:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
        self.target_image = pygame.transform.scale(pygame.image.load("D:\\2023\\Semester 3\\Grafika Komputer\\Orion\\graphics\\gameplay\\target.png").convert_alpha(), (50, 50))

        # Membuat objek Player
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        self.asset_basicAttack_Player = self.player.basic_attack_path

        # Inisialisasi list untuk menyimpan serangan dasar
        self.basic_attacks = []

        # Inisialisasi 3 target dengan gambar yang telah Anda sediakan
        self.targets = []
        target_x_positions = [400, 500, 600]  # Atur posisi target sesuai kebutuhan
        for x in target_x_positions:
            target = Target(x, 50, self.target_image)
            self.targets.append(target)

    def run(self):
        current_time = pygame.time.get_ticks()

        # Cek apakah sudah waktunya untuk serangan dasar baru
        if current_time - self.last_attack_time >= 500:
            self.create_basic_attack()  # Membuat serangan dasar baru
            self.last_attack_time = current_time  # Perbarui waktu serangan terakhir

        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Gambar kembali objek pemain
        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Menggambar dan mengupdate serangan dasar
        for attack in self.basic_attacks:
            attack.update()
            attack.draw(self.screen)

            # Periksa tabrakan dengan target
            for target in self.targets:
                if attack.rect.colliderect(target.rect):
                    # self.targets.remove(target)
                    ic(attack.rect.colliderect(target.rect))
                    print("kena cuk")

        # Menggambar target
        for target in self.targets:
            target.draw(self.screen)

        # Draw player health bar and score
        self.player.draw_health_bar(self.screen)
        self.player.draw_score(self.screen)

        # Draw countdown cooldown text
        cooldown_text = self.player.font.render(self.player.skill_cooldown_text, True, (255, 255, 255))
        self.screen.blit(cooldown_text, (10, 10))

    def create_basic_attack(self):
        # Membuat serangan dasar baru dan menambahkannya ke daftar serangan dasar
        basic_attack = BasicAttack(self.player, damage=10, speed=20, image=pygame.transform.scale((pygame.image.load(self.asset_basicAttack_Player)),(50,50)), direction="up")
        self.basic_attacks.append(basic_attack)