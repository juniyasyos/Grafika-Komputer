import pygame
import os
from icecream import ic

def load_image(image_filename, path=False):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar
    
    if path:
        return image_path

    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, screen):
        super().__init__()

        # Load player image and get its rect
        image = load_image("../resources/assets/Battle/PLAYER.png")
        self.basic_attack = load_image("../resources/assets/Battle/bullet.png")
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect()
        self.screen = screen

        # Set initial position
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10

        self.current_time = 0

        # Set player attributes
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.damage = 0

        self.skill_cooldown_timer = 0  # Waktu countdown cooldown skill
        self.skill_cooldown_text = ""  # Teks countdown
        self.font = pygame.font.Font(None, 36)  # Font untuk teks countdown

        # Player abilities/skills
        self.skills = {
            "speed_boost": {"active": False, "cooldown": 0, "duration": 5, "last_used": 0},
            "shield": {"active": False, "cooldown": 0, "duration": 10, "last_used": 0},
        }

    def get_damage(self, damage=10):
        return self.damage + damage

    def handle_events(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.use_skill("speed_boost")
        if keys[pygame.K_LSHIFT]:
            self.use_skill("shield")
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed
        # ic(self.rect)
        

    def update(self, screen_width, screen_height, speed):
        self.handle_events(speed=speed)

        # Draw player health bar and score
        self.draw_health_bar(self.screen)
        self.draw_score(self.screen)

        # Draw countdown cooldown text
        cooldown_text = self.font.render(self.skill_cooldown_text, True, (0, 0, 0))
        self.screen.blit(cooldown_text, (100, 100))  # Ganti posisi sesuai kebutuhan

        if self.skill_cooldown_timer > 0:
            self.skill_cooldown_timer -= 1
            self.skill_cooldown_text = str(self.skill_cooldown_timer // 60 + 1)  # Hitung detik tersisa
        else:
            self.skill_cooldown_text = ""  # Cooldown telah selesai
        # ic(self.skill_cooldown_text)

        # Keep player within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

        # Draw player
        self.screen.blit(self.image, self.rect)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            # Player is defeated, handle game over logic here

    def use_skill(self, skill_name):
        if self.skills[skill_name]["cooldown"] == 0 and not self.skills[skill_name]["active"]:
            # Activate the skill and set cooldown
            self.skills[skill_name]["active"] = True
            self.skills[skill_name]["cooldown"] = self.skills[skill_name]["duration"]
            # ic(self.skills)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, current_health_width, 5))

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    def create_basic_attack_player(self, BasicAttack, player):
        # Membuat serangan dasar baru dan menambahkannya ke daftar serangan dasar
        basic_attack = BasicAttack(player, damage=10, speed=20, image=pygame.transform.scale((self.basic_attack),(30,30)), direction="up")
        return basic_attack
