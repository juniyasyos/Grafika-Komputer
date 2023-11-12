from .. import gameplay as gp

class Player:
    def __init__(self, screen_width, screen_height, screen):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load player image and get its rect
        self.image = gp.load_image("../resources/assets/Battle/PLAYER.png",size=(100,100), colorkey=("white"))
        self.image_rocket = gp.load_image("../resources/assets/Battle/Rocket/Rocket_061.png", scale=50)
        self.rect = self.image.get_rect()
        self.font = gp.pygame.font.Font(None, 36)

        # Set initial position
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10

        # Player attributes
        self.speed = 18
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.damage = 100
        self.last_BasicAttack_time = 0
        self.shield = 50
        self.max_shield = 50
        self.delay_basicAttack = 200
        self.regen_hp = 0.007
        self.basicAttack_func = None
        self.type_basicAttack = "type_1"
        self.basic_attack_speed = 4
        self.player_basic_attacks = gp.pygame.sprite.Group() 
        self.basic_attack_path = gp.load_image("../resources/assets/Battle/Laser Sprites/11.png")

        # Player skills
        self.skills = {
            "1": {"speed": {"active": False, "cooldown": 9000, "duration": 5000, "last_used": 0, "used": 0}},
            "2": {"masif_ba": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "3": {"rocket": {"active": False, "cooldown": 30000, "duration": 5000, "last_used": 0, "used": 0}},
            "4": {"shield": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "SPACE": {"regen": {"active": False, "cooldown": 30000, "duration": 2000, "last_used": 0, "used": 0}}
        }

    def handle_events(self):
        keys = gp.pygame.key.get_pressed()
        if keys[gp.pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[gp.pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[gp.pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[gp.pygame.K_DOWN]:
            self.rect.y += self.speed

        for skill_key, skill_data in self.skills.items():
            for skill_name, skill_data in skill_data.items():
                if keys[gp.pygame.key.key_code(skill_key)]:
                    if self.current_time - skill_data["last_used"] >= skill_data["cooldown"] or skill_data["last_used"] == 0:
                        if not skill_data["active"]:
                            skill_data["last_used"] = self.current_time
                            skill_data["active"] = True
                            skill_data["used"] += 1

        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def update(self):
        self.current_time = gp.pygame.time.get_ticks()
        self.handle_events()
        self.skill_use()
        self.draw_health_bar()
        self.draw_score()
        self.draw_icon_skill()
        self.set_basicAttack_func()
        self.screen.blit(self.image, self.rect)

        for attack in self.player_basic_attacks:
            attack.update()

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
                        gp.pygame.draw.circle(self.screen, "blue", (self.rect.x + 35, self.rect.y + 25), 70)
                if skill_name == "rocket":
                    pass
                if skill_name == "masif_ba":
                    self.type_basicAttack = "type_2" if skill_data["active"] else "type_1"
                    # self.delay_basicAttack = 100 if skill_data["active"] else 200

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
        gp.pygame.draw.rect(self.screen, color[0], (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (show[0] / show[1]) * self.rect.width
        gp.pygame.draw.rect(self.screen, color[1], (self.rect.x, self.rect.y - 10, current_health_width, 5))

    def draw_score(self):
        text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def create_basic_attack_player(self, BasicAttack, player, last_time):
        if self.current_time - last_time >= self.delay_basicAttack:
            self.player_basic_attacks.add(
                BasicAttack(
                    screen=self.screen,
                    actor=player, 
                    speed=self.basic_attack_speed, 
                    image=gp.pygame.transform.scale(self.basic_attack_path, (30, 30)), 
                    direction="up",
                    attack_type="Spesial",
                    func=self.basicAttack_func
                    )
                )
            self.last_BasicAttack_time = self.current_time

    def draw_icon_skill(self):
        for i, (skill_key, skill_data) in enumerate(self.skills.items(), start=1):
            for skill_name, skill_data in skill_data.items():
                calculate_cooldown = lambda skill_data, current_time: max(0, ((skill_data["last_used"] - self.current_time) + skill_data["cooldown"]) // 1000) if skill_data["used"] != 0 else 0
                cooldown = calculate_cooldown(skill_data, self.current_time)

                gp.pygame.draw.rect(self.screen, "white", [10, 70 + i * 60, 150, 50])
                text = self.font.render(f"{skill_name}: {cooldown}", True, "black")
                self.screen.blit(text, (10, 80 + i * 60))
    
    def set_basicAttack_func(self):
        def type_1(screen):
            for attack in self.player_basic_attacks:
                attack.rect.y -= attack.speed
                screen.blit(attack.image, (attack.rect.x, attack.rect.y))

        def type_2(screen):
            for index, attack in enumerate(self.player_basic_attacks):
                if index % 2 == 0 and index != 0:
                    attack.rect.y -= attack.speed
                    screen.blit(attack.image, (attack.rect.x+10, attack.rect.y))
                else:
                    attack.rect.y -= attack.speed
                    screen.blit(attack.image, (attack.rect.x-10, attack.rect.y))
                
        
        if self.type_basicAttack == "type_1":
            func = type_1
        elif self.type_basicAttack == "type_2":
            func = type_2

        self.basicAttack_func = func
        

