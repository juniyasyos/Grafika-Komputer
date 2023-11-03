import pygame
import os
from icecream import ic
import threading

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar
    
    try:
        image = pygame.image.load(image_path).convert_alpha()
        image = image.convert()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e

class Player():
    def __init__(self, screen_width, screen_height, screen):
        super().__init__()

        # Load player image and get its rect
        self.image = pygame.transform.scale(load_image("../resources/assets/Battle/PLAYER.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.screen = screen
        self.font = pygame.font.Font(None, 24)

        # Set initial position
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10

        # Player attributes
        self.speed = 8
        self.health = self.max_health = 100
        self.score = 0
        self.damage = 10
        self.last_BasicAttack_time = 0
        self.shield = 50
        self.regen_hp = 0.5
        self.basic_attack_path = load_image("../resources/assets/Battle/bullet.png")

        # Player skills
        self.skills = {
            "1": {"speed": {"active": False, "cooldown": 9000, "duration": 5000, "last_used": 0, "used": 0}},
            "4": {"shield": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "3": {"rocket": {"active": False, "cooldown": 30000, "duration": 5000, "last_used": 0, "used": 0}},
            "SPACE": {"regen": {"active": False, "cooldown": 50000, "duration": 10000, "last_used": 0, "used": 0}},
            "2": {"masif_basic_attack": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}}
        }

    def handle_events(self, current_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Kontrol keterampilan
        for skill_key, skill_data in self.skills.items():
            # ic(keys[pygame.key.key_code(skill_key)])
            if keys[pygame.key.key_code(skill_key)]:
                for skill_name, skill_data in skill_data.items():
                    if current_time - skill_data["last_used"] >= skill_data["cooldown"] or skill_data["last_used"] == 0:
                        if not skill_data["active"]:
                            skill_data["last_used"] = current_time
                            skill_data["active"] = True
                            skill_data["used"] += 1
                            

    def update(self):
        current_time = pygame.time.get_ticks()
        event = lambda: self.handle_events(current_time)

        # Gambar batang kesehatan dan skor pemain
        health_bar = lambda: self.draw_health_bar()
        score = lambda: self.draw_score()
        icon_skill = lambda: self.draw_icon_skill(current_time=current_time)

        def skill_use():
            # Loop untuk memproses skills
            for skill_key, skill_data in self.skills.items():
                for skill_name, skill_data in skill_data.items():
                    # Logic Skill
                    if skill_name == "speed":
                        self.speed = 20 if skill_data["active"] else 10
                        if current_time - skill_data["last_used"] >= skill_data["duration"]:
                            skill_data["active"] = False

        # Pastikan pemain tetap dalam batasan layar
        self.rect.x = max(0, min(self.rect.x, self.screen.get_width() - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen.get_height() - self.rect.height))

        # Gambar pemain
        self.screen.blit(self.image, self.rect)

        # Pemanfaatan threading         
        threads = []
        for operation in [event, health_bar, score, icon_skill, skill_use]:
            thread = threading.Thread(target=operation)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
                
    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, current_health_width, 5))

    def draw_score(self):
        text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def create_basic_attack_player(self, BasicAttack, player, amount_BasicAttack, current_time, last_time):
        if  current_time - last_time >= 500:
            return BasicAttack(player, damage=10, speed=20, image=pygame.transform.scale(self.basic_attack_path, (30, 30)), direction="up")
        return None

    def draw_icon_skill(self, current_time):
        for i, (skill_key, skill_data) in enumerate(self.skills.items(), start=1):
            for skill_name, skill_data in skill_data.items():
                # Set Cooldown skill
                calculate_cooldown = lambda skill_data, current_time: max(0, ((skill_data["last_used"] - current_time) + skill_data["cooldown"]) // 1000) if skill_data["used"] != 0 else 0
                cooldown = calculate_cooldown(skill_data, current_time)
                
                # Show cooldown skill
                pygame.draw.rect(self.screen, "white", [10, 70 + i * 60, 150, 50])
                text = self.font.render(f"{skill_name}: {cooldown}", True, "black")
                self.screen.blit(text, (10, 80 + i * 60))
