import pygame
from .player import Player
from .enemy import obj_Enemy, EnemyType1
from .. import gameplay as gp

class AttackActor(pygame.sprite.Sprite):
    def __init__(self, actor, damage, speed, image, direction):
        super().__init__()
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

class Battle:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.start_game = pygame.time.get_ticks()

        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)
        self.player_basic_attacks = pygame.sprite.Group()
        self.enemy_basic_attacks = pygame.sprite.Group()

        # Membuat objek Enemy dan elemennya
        self.enemies = pygame.sprite.Group()

    def run_battle(self):
        self.current_time = pygame.time.get_ticks()
        self.create_enemy()
        self.player.update()
        self.attack_player()
        self.attack_enemy()
        self.remove_elemen_obj()
        self.cek_basic_attack()

    def attack_player(self):
        for attack in self.player_basic_attacks:
            attack.update()
            self.screen.blit(attack.image, attack.rect)

    def attack_enemy(self):
        for attack in self.enemy_basic_attacks:
            self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))
            attack.update()

    def remove_elemen_obj(self):
        self.player_basic_attacks = pygame.sprite.Group(
            [attack for attack in self.player_basic_attacks if attack.rect.y > 0]
        )
        self.enemy_basic_attacks = pygame.sprite.Group(
            [attack for attack in self.enemy_basic_attacks if attack.rect.y < self.screen_height]
        )

    def cek_basic_attack(self):
        for enemy in self.enemies:
            enemy_basic_attack = enemy.create_basic_attack_enemy(AttackActor, enemy, self.current_time, enemy.last_BasicAttack_time, cooldown_basicAttack=gp.random.randint(2000, 5000))
            if enemy_basic_attack is not None:
                self.enemy_basic_attacks.add(enemy_basic_attack)
                enemy.last_BasicAttack_time = self.current_time

        player_basic_attack = self.player.create_basic_attack_player(AttackActor, self.player,  self.player.last_BasicAttack_time)
        if player_basic_attack is not None:
            self.player_basic_attacks.add(player_basic_attack)
            self.player.last_BasicAttack_time = self.current_time

    def create_enemy(self):
        for enemy in self.enemies:
            if self.current_time - self.start_game >= enemy.delay_to_next_path[0]:
                enemy.draw(self.screen)
                enemy.draw_health()
                enemy_attack = False

                for attack in self.player_basic_attacks:
                    if enemy.health <= 0:
                        if enemy in self.enemies: 
                            self.enemies.remove(enemy)
                            self.player.score += 1
                    if attack.rect.colliderect(enemy.rect):
                        enemy.health -= self.player.damage
                        self.player_basic_attacks.remove(attack)

            for enemy in self.enemies:
                for attack in self.enemy_basic_attacks:
                    if attack.rect.colliderect(self.player.rect):
                        self.player.take_damage(enemy.damage)
                        self.enemy_basic_attacks.remove(attack)

                remove_enemy = enemy.update()
                if remove_enemy is True or enemy.path_index >= len(enemy.path):
                    self.enemies.remove(enemy)

class level_1(Battle):
    def __init__(self, screen, screen_height, screen_width):
        super().__init__(screen, screen_height, screen_width)
        self.stage_index = 0
        self.stage_delay =  pygame.time.get_ticks()
        self.stage = {
            "Stage 1": [
                EnemyType1(screen=self.screen, path=[(100, 100), (300, 50), (self.player.rect.x, self.player.rect.y)], delay=[1000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 50), (450, 100), (self.screen_width, 100)], delay=[2000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (550, 50), (self.screen_width, 200)], delay=[3000, 30000, 0]),
            ],
            "Stage 2": [
                EnemyType1(screen=self.screen, path=[(300, 50), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[0, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 50), (500, 50), (self.screen_width, 100)], delay=[2000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[3000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[4000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[5000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (90, 50), (self.screen_width, 200)], delay=[6000, 30000, 0]),
            ],
            "Stage 3": [
                EnemyType1(screen=self.screen, path=[(0, 0), (400, 50), (self.player.rect.x, self.player.rect.y)], delay=[100, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (500, 50), (self.screen_width, 100)], delay=[2000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (600, 50), (self.screen_width, 200)], delay=[3000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (700, 50), (self.screen_width, 200)], delay=[4000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (800, 50), (self.screen_width, 200)], delay=[5000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (900, 50), (self.screen_width, 200)], delay=[6000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (1000, 50), (self.screen_width, 200)], delay=[7000, 30000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (1100, 50), (self.screen_width, 200)], delay=[8000, 30000, 0]),
            ],
            "delay": [0, 9000, 10000]
        }

    def run(self):
        if len(self.enemies) == 0:
            if self.stage_index+1 < len(self.stage):
                if pygame.time.get_ticks() - self.stage_delay >= self.stage["delay"][self.stage_index]:
                    self.stage_index += 1
                    self.enemies = pygame.sprite.Group(self.stage[f"Stage {self.stage_index}"])
                    self.stage_delay = pygame.time.get_ticks()
        self.run_battle()
