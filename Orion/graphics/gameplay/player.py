import pygame
import os
from icecream import ic
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

class Player:
    def __init__(self, screen_width, screen_height, screen):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load player image and get its rect
        self.image = pygame.transform.scale(load_image("../resources/assets/Battle/PLAYER.png"), (70, 70))
        self.image_rocket = pygame.transform.scale(load_image("../resources/assets/Battle/Rocket/Rocket_061.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 36)

        # Set initial position
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10

        # Player attributes
        self.speed = 18
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.damage = 10
        self.last_BasicAttack_time = 0
        self.shield = 50
        self.max_shield = 50
        self.regen_hp = 0.007
        self.basic_attack_path = load_image("../resources/assets/Battle/bullet.png")

        # Player skills
        self.skills = {
            "1": {"speed": {"active": False, "cooldown": 9000, "duration": 5000, "last_used": 0, "used": 0}},
            "2": {"masif_ba": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "3": {"rocket": {"active": False, "cooldown": 30000, "duration": 5000, "last_used": 0, "used": 0}},
            "4": {"shield": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "SPACE": {"regen": {"active": False, "cooldown": 30000, "duration": 2000, "last_used": 0, "used": 0}}
        }

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        for skill_key, skill_data in self.skills.items():
            for skill_name, skill_data in skill_data.items():
                if keys[pygame.key.key_code(skill_key)]:
                    if self.current_time - skill_data["last_used"] >= skill_data["cooldown"] or skill_data["last_used"] == 0:
                        if not skill_data["active"]:
                            skill_data["last_used"] = self.current_time
                            skill_data["active"] = True
                            skill_data["used"] += 1

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_events()

        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

        self.skill_use()
        self.draw_health_bar()
        self.draw_score()
        self.draw_icon_skill()

        self.screen.blit(self.image, self.rect)

    def skill_use(self):
        for skill_key, skill_data in self.skills.items():
            for skill_name, skill_data in skill_data.items():
                if skill_name == "speed":
                    self.speed = 30 if skill_data["active"] else 18
                if skill_name == "regen" and not self.health > self.max_health:
                    if skill_data["active"]:
                        self.health += self.max_health * self.regen_hp
                if skill_name == "shield":
                    if skill_data["active"]:
                        pygame.draw.circle(self.screen, "blue", (self.rect.x + 35, self.rect.y + 25), 70)
                if skill_name == "rocket":
                    pass
                if skill_name == "masif_basic_attack":
                    pass

                if self.current_time - skill_data["last_used"] >= skill_data["duration"]:
                    skill_data["active"] = False

    def take_damage(self, damage=10):
        if self.skills["4"]["shield"]["active"] and self.shield >= 0:
            self.shield -= damage
            self.shield = max(self.shield, 0)
        else:
            self.health -= damage
            self.health = max(self.health, 0)

    def draw_health_bar(self):
        color = ["green", "cyan"] if self.skills["4"]["shield"]["active"] and self.shield >= 0 else ["red", "green"]
        show = [self.shield, self.max_shield] if self.skills["4"]["shield"]["active"] and self.shield >= 0 else [self.health, self.max_health]
        pygame.draw.rect(self.screen, color[0], (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (show[0] / show[1]) * self.rect.width
        pygame.draw.rect(self.screen, color[1], (self.rect.x, self.rect.y - 10, current_health_width, 5))

    def draw_score(self):
        text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def create_basic_attack_player(self, BasicAttack, player, amount_BasicAttack, last_time):
        if self.current_time - last_time >= 300:
            return BasicAttack(player, damage=10, speed=20, image=pygame.transform.scale(self.basic_attack_path, (30, 30)), direction="up")
        return None

    def draw_icon_skill(self):
        for i, (skill_key, skill_data) in enumerate(self.skills.items(), start=1):
            for skill_name, skill_data in skill_data.items():
                calculate_cooldown = lambda skill_data, current_time: max(0, ((skill_data["last_used"] - self.current_time) + skill_data["cooldown"]) // 1000) if skill_data["used"] != 0 else 0
                cooldown = calculate_cooldown(skill_data, self.current_time)

                pygame.draw.rect(self.screen, "white", [10, 70 + i * 60, 150, 50])
                text = self.font.render(f"{skill_name}: {cooldown}", True, "black")
                self.screen.blit(text, (10, 80 + i * 60))

