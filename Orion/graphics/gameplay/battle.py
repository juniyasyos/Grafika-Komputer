from .player import Player
from .enemy import obj_Enemy, EnemyType1
from .. import gameplay as gp

class Explosion(gp.pygame.sprite.Sprite):
    def __init__(self, x, y, explosion_images):
        super().__init__()
        self.images = explosion_images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = gp.pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = gp.pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center=self.rect.center)

class AttackActor(gp.pygame.sprite.Sprite):
    def __init__(self, screen, actor, speed, image, direction, attack_type="basic", func=None):
        super().__init__()
        self.screen = screen
        self.actor = actor
        self.speed = speed
        self.image = image
        self.direction = direction
        self.attack_type = attack_type
        self.func = func

        self.rect = self.image.get_rect()
        self.rect.center = actor.rect.center

    def update(self):
        if self.attack_type == "basic":
            self.update_basic_attack()
        if self.attack_type == "rocket":
            self.update_rocket()
        if self.attack_type == "laser":
            self.update_laser()

    def update_basic_attack(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

    def update_rocket(self):
        pass

    def update_laser(self):
        pass

class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.start_game = gp.pygame.time.get_ticks()

        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)

        # Membuat objek Enemy dan elemennya
        self.enemies = gp.pygame.sprite.Group()
        self.explosions = gp.pygame.sprite.Group()
        self.image_explosion = [
            gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion3/{i+1}.png",size=(50,50), scale=2) for i in range(30)
        ]
        self.bullet_explosions = gp.pygame.sprite.Group()
        self.bullet_explosions_image = [
            gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion4/{i+1}.png",size=(15,15), scale=2) for i in range(25)
        ]

    def run_battle(self):
        self.current_time = gp.pygame.time.get_ticks()
        self.explosions.update()
        self.bullet_explosions.update()
        self.create_enemy()
        self.player.update()
        self.attack_enemy()
        self.remove_elemen_obj()
        self.cek_basic_attack()
        self.explosions.draw(self.screen)
        self.bullet_explosions.draw(self.screen)

    def attack_enemy(self):
        for enemy in self.enemies:
            for attack in enemy.enemy_basic_attacks:
                self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))
                attack.update()

    def remove_elemen_obj(self):
        for attacks_d in self.player.player_basic_attacks:
                gp.pygame.sprite.Group([attack for attack in attacks_d if attack.rect.y > 0])

        for enemy in self.enemies:
            enemy.enemy_basic_attacks = gp.pygame.sprite.Group(
                [attack for attack in enemy.enemy_basic_attacks if attack.rect.y < self.screen_height]
            )

    def cek_basic_attack(self):
        if self.enemies:
            for enemy in self.enemies:
                enemy.create_basic_attack_enemy(AttackActor, enemy, self.current_time, enemy.last_BasicAttack_time, cooldown_basicAttack=gp.random.randint(2000, 5000))
            self.player.createe_basic_attack_player(AttackActor, self.player,  self.player.last_BasicAttack_time)

    def create_enemy(self):
        for enemy in self.enemies:
            if self.current_time - self.start_game >= enemy.delay_to_next_path[0]:
                enemy.draw(self.screen)
                enemy.draw_health()
                enemy_attack = False

                for attacks in self.player.player_basic_attacks:
                    for attack in attacks:
                        if enemy.health <= 0:
                            if enemy in self.enemies: 
                                for jml_explosions in range(gp.random.randint(1,3)):
                                    self.explosions.add(Explosion(x=enemy.rect.x+gp.random.randint(-50,50), y=enemy.rect.y+gp.random.randint(-50,50), explosion_images=self.image_explosion))
                                self.player.score += 1
                                self.enemies.remove(enemy)
                                
                        if attack.rect.colliderect(enemy.rect):
                            enemy.health -= self.player.damage
                            self.bullet_explosions.add(Explosion(x=attack.rect.x, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                            attacks.remove(attack)
                            
            for enemy in self.enemies:
                for attack in enemy.enemy_basic_attacks:
                    if attack.rect.colliderect(self.player.rect):
                        self.player.take_damage(enemy.damage)
                        self.bullet_explosions.add(Explosion(x=attack.rect.x, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                        enemy.enemy_basic_attacks.remove(attack)

                remove_enemy = enemy.update()
                if remove_enemy is True or enemy.path_index >= len(enemy.path):
                    self.enemies.remove(enemy)


class level_1(Battle):
    def __init__(self, screen, screen_height, screen_width):
        super().__init__(screen, screen_height, screen_width)
        self.stage_index = 0
        self.stage_delay =  gp.pygame.time.get_ticks()
        self.stage = {
            "Stage 1": [
                EnemyType1(screen=self.screen, path=[(100, 100), (300, 50), (self.player.rect.x, self.player.rect.y)], delay=[1000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 50), (450, 100), (self.screen_width, 100)], delay=[1500, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (550, 50), (self.screen_width, 200)], delay=[2000, 35000, 0]),
            ],
            "Stage 2": [
                EnemyType1(screen=self.screen, path=[(0, 0), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[1000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (500, 50), (self.screen_width, 100)], delay=[2000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[3000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[4000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[5000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (900, 50), (self.screen_width, 200)], delay=[6000, 35000, 0]),
            ],
            "Stage 3": [
                EnemyType1(screen=self.screen, path=[(0, 0), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[1000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (500, 50), (self.screen_width, 100)], delay=[2000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[3000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[4000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[5000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (900, 50), (self.screen_width, 200)], delay=[6000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (1000, 50), (self.screen_width, 200)], delay=[7000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (1100, 50), (self.screen_width, 200)], delay=[8000, 35000, 0]),
            ],
            "delay": [0, 9000, 10000]
        }

    def run(self):
        if len(self.enemies) == 0:
            if self.stage_index+1 < len(self.stage):
                if gp.pygame.time.get_ticks() - self.stage_delay >= self.stage["delay"][self.stage_index]:
                    self.stage_index += 1
                    self.enemies = gp.pygame.sprite.Group(self.stage[f"Stage {self.stage_index}"])
                    self.stage_delay = gp.pygame.time.get_ticks()
        self.run_battle()
