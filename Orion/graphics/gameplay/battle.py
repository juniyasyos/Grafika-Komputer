from .player import Player
from .enemy import EnemyType1, EnemyType2, EnemyBoss
from .. import gameplay as gp
import pygame
import os
import random
from .friends import Friends
import numpy as np

# class objek ledakan.
class Explosion(pygame.sprite.Sprite):
    # initialisasi ledakan actor
    def __init__(self, x, y, explosion_images):
        """
        Inisialisasi objek ledakan.

        Parameters:
        - x (int): Koordinat x untuk menempatkan ledakan.
        - y (int): Koordinat y untuk menempatkan ledakan.
        - explosion_images (list): Daftar gambar ledakan.

        Attributes:
        - images (list): Daftar gambar ledakan.
        - image (Surface): Gambar ledakan saat ini.
        - rect (Rect): Area persegi panjang yang mengelilingi gambar ledakan.
        - frame (int): Indeks gambar ledakan saat ini.
        - last_update (int): Waktu terakhir pembaruan frame.
        - frame_rate (int): Kecepatan perubahan frame (milidetik).
        
        Methods:
        - update (self) : memperbarui objek ledakan.
        """
        
        super().__init__()
        self.images = explosion_images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    # Update animasi ledakan
    def update(self):
        """
        Memperbarui objek ledakan pada setiap frame.
        Jika sudah mencapai frame terakhir, objek akan dihapus (kill).
        Pembaruan frame terjadi berdasarkan kecepatan frame_rate.
        """
        
        # Mendapatkan waktu sekarang dalam milidetik
        now = pygame.time.get_ticks()
        
        # Memeriksa apakah sudah waktunya untuk memperbarui frame ledakan
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=  1
            
            # Memeriksa apakah sudah mencapai frame terakhir
            if self.frame == len(self.images):
                # Jika ya, menghapus objek ledakan (kill)
                self.kill()
            else:
                # Jika belum, memperbarui gambar dan posisi objek ledakan berdasarkan frame
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center = self.rect.center)


# Inisialisasi objek serangan actor.
class AttackActor(pygame.sprite.Sprite):
    """
        Inisialisasi objek serangan actor.

        Parameters:
        - screen (Surface): Layar game.
        - actor (Actor): Objek aktor yang melakukan serangan.
        - speed (int): Kecepatan pergerakan serangan.
        - image (Surface): Gambar serangan.
        - attack_type (str): Jenis serangan (default: "basic").
        - func (function): Fungsi khusus terkait serangan (default: None).

        Attributes:
        - screen (Surface): Layar game.
        - actor (Actor): Objek aktor yang melakukan serangan.
        - speed (int): Kecepatan pergerakan serangan.
        - image (Surface): Gambar serangan.
        - attack_type (str): Jenis serangan.
        - func (function): Fungsi khusus terkait serangan.
        - rect (Rect): Area persegi panjang yang mengelilingi gambar serangan,
          diatur pada posisi awal aktor.
          
        Methods:
        - update (self) : update semua serangan yang dimiliki oleh user kecuali basic attack
        - update_rocket (self) : update serangan khusus roket penjelajah
        - update_laser (self) : update serangan basic attack tanpa celah
        """
        
    def __init__(self, screen, actor, speed, image, attack_type="basic", func = None, target_position=(0,0)):
        super().__init__()
        self.screen = screen
        self.actor = actor
        self.speed = speed
        self.image = image
        self.attack_type = attack_type
        self.func = func

        self.rect = self.image.get_rect()
        self.rect.center = actor.rect.center

    def update(self):
        """
        Memperbarui objek serangan pada setiap frame berdasarkan jenis serangan.
        """
        if self.attack_type == "rocket":
            self.update_rocket()
        if self.attack_type == "laser":
            self.update_laser()



# Kelas untuk mengelola pertempuran dalam permainan.
class Battle:
    # Initialisasi objeck dalam battle
    def __init__(self, screen, screen_width, screen_height, image_background, stage, level_path, next_level):
        """
        Kelas untuk mengelola pertempuran dalam permainan.

        Args:
        - screen (Surface): Objek layar permainan.
        - screen_width (int): Lebar layar permainan.
        - screen_height (int): Tinggi layar permainan.
        - image_background: Gambar latar belakang pertempuran.
        - stage: Objek stage.

        Attributes:
        - screen (Surface): Objek layar permainan.
        - screen_width (int): Lebar layar permainan.
        - screen_height (int): Tinggi layar permainan.
        - start_game (int): Waktu mulai permainan.
        - player (Player): Objek player.
        - enemies (Group): Grup objek musuh.
        - explosions (Group): Grup objek ledakan.
        - image_explosion (list): Daftar gambar ledakan.
        - bullet_explosions (Group): Grup objek ledakan peluru.
        - bullet_explosions_image (list): Daftar gambar ledakan peluru.
        - stage_index (int): Indeks stage.
        - __start (int): Waktu mulai looping internal.
        - path_delay (int): Waktu tunda path.
        - next_stage_delay (int): Waktu tunda menuju stage berikutnya.
        - path_image_background: Gambar latar belakang path.
        - kill_player_delay (int): Waktu tunda pembunuhan player.
        - stage: Objek stage.
        - sound_files (dict): File suara permainan.

        Methods:
        - run_battle (self): Menjalankan pertempuran.
        - enemy_update (self): Update musuh.
        - remove_elemen_obj (self): Menghapus elemen objek.
        - cek_actor_attack (self): Memeriksa serangan actor.
        - create_enemy (self): Membuat musuh baru.
        """
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.start_game = pygame.time.get_ticks()

        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen = self.screen)
        self.kill_player_delay = 0 

        # Membuat objek Enemy dan elemennya
        self.enemies = pygame.sprite.Group()

        # Elemen global
        self.explosions = pygame.sprite.Group()
        self.image_explosion = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion3/{i+1}.png",size = (50,50), scale = 2) for i in range(30)]
        self.bullet_explosions = pygame.sprite.Group()
        self.bullet_explosions_image = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion4/{i+1}.png",size = (15,15), scale = 2) for i in range(25)]
        self.stage_index = 0
        self.__start = 0
        self.path_delay =  pygame.time.get_ticks()
        self.next_stage_delay = 0
        self.path_image_background = image_background   
        self.stage = stage
        self.level_path = level_path
        self.next_level = next_level
        
        # Elemen Suara
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.play_sound = True
        self.sound_files = {
            "win sound": pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/win sound.mp3")),
            "lose sound": pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/lose sound.mp3")),
            "battle sound" : pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/battle sound .mp3"))
        }
        for sound in self.sound_files.values():
            sound.set_volume(0.3)
    
    def save_data(self):
        save_data = gp.load_from_json("../resources/save_data.json")
        if self.player.score >= 10:
            print("masuk")
            save_data[self.level_path][0] = self.player.score
            save_data[self.next_level][1] = "True"
            gp.save_to_json("../resources/save_data.json", save_data)
    
    # Animasi perubahan transparansi layar menjadi hitam.
    def fade_animation(self):
        """
        Animasi perubahan transparansi layar menjadi hitam.

        Notes:
        - Fungsi ini mengubah transparansi layar dari 0 hingga 255 dengan interval 5.
        - Setelah itu, menghentikan semua suara.
        """
        black_surface = pygame.Surface((self.screen_width, self.screen_height))
        black_surface.fill(pygame.Color("black"))

        for alpha in range(0, 256, 5):
            black_surface.set_alpha(alpha)
            self.screen.blit(black_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(4000 // (256 // 6))

        for sound in self.sound_files.values():
            sound.stop()

    # Menjalankan Pertempuran.
    def run(self, play_sound):
        """
        Menjalankan pertempuran.

        Args:
        - play_sound (bool): Status pemutaran suara.

        Returns:
        - bool: Status permainan (True jika selesai, False jika pemain kalah, None jika permainan berlanjut).
        """
        current_time = pygame.time.get_ticks()

        if play_sound and self.play_sound:
            self.sound_files["battle sound"].play(maxtime=-1)
            self.play_sound = False

        if len(self.enemies) == 0:  # mengecek apakah ada musuh
            if self.stage_index + 1 < len(self.stage):  # mengecek apakah masih ada stage yg tersisa
                stage_delay = self.stage["delay"][self.stage_index]
                if current_time - self.next_stage_delay >= stage_delay:
                    self.prepare_next_stage(current_time)
                    
            elif self.stage_index + 1 == len(self.stage):   # Mengecek apakah stage sudah urutan yg terakhir 
                finish_delay = 6000
                if current_time - self.next_stage_delay >= finish_delay:
                    self.stage_index += 1

        if self.player.health <= 0: # Player lose
            finish_delay = 7000
            if self.handle_player_loss(current_time, finish_delay):
                return False

        elif self.stage_index >= len(self.stage):   # Player win
            finish_delay = 5000
            if self.handle_player_win(current_time, finish_delay):
                self.save_data()
                return True
            
        else:   # pertempuran belum berakhir
            self.handle_battle_continue(current_time)

    # Persiapan menuju stage selanjutnya
    def prepare_next_stage(self, current_time):
        self.stage_index += 1
        self.enemies = pygame.sprite.Group(*self.stage[f"Stage {self.stage_index}"])
        self.path_delay = current_time
        self.next_stage_delay = self.path_delay + self.stage["delay"][self.stage_index - 1]

    # handle action player kalah
    def handle_player_loss(self, current_time, finish_delay):
        self.sound_files["battle sound"].stop()
        if self.start == 0:
            self.start += 1
            self.sound_files["lose sound"].play()

        if current_time - self.kill_player_delay >= finish_delay:
            return True
        elif current_time - self.kill_player_delay >= 2500:
            self.sound_files["battle sound"].stop()
            self.fade_animation()
        else:
            self.player_death(current_time)
    
    # aksi yang dilakukan ketika player menang
    def handle_player_win(self, current_time, finish_delay):
        self.sound_files["battle sound"].stop()

        if self.start == 0:
            self.start += 1
            self.sound_files["win sound"].play() 

        if current_time - self.kill_player_delay >= finish_delay:
            return True
        elif current_time - self.kill_player_delay >= 1000:
            self.sound_files["battle sound"].stop()
            self.fade_animation()
        else:
            self.player_finish(current_time)
    
    # handle action player mati
    def player_death(self, current_time):
        self.player.handle_option = False
        self.run_battle()
        self.player.player_basic_attacks.clear()

        if current_time % 20 == 0:
            self.explosions.add(Explosion(x=self.player.rect.x + random.randint(-30, 30) + 50,
                                        y=self.player.rect.y + random.randint(-30, 30) + 40,
                                        explosion_images=self.image_explosion))
    
    # handle oction player memenangkan pertarungan
    def player_finish(self, current_time):
        self.player.handle_option = False
        self.run_battle()
        self.player.player_basic_attacks.clear()
        
        self.handle_option = False
        if self.player.rect.y >= -100:
            self.player.rect.y -= self.player.speed
    
    # handle action pertempuran masih berlanjut
    def handle_battle_continue(self, current_time):
        self.run_battle()
        self.start = 0
        self.kill_player_delay = pygame.time.get_ticks()

        if self.position_player[1] >= 0 and self.stage_index == len(self.stage):
            self.player.rect.y -= self.player.speed

        if self.position_player[1] < 0:
            self.stage_index += 1
    
    # Menjalankan update pertempuran.
    def run_battle(self):
        """
        Menjalankan update pertempuran.

        Notes:
        - Memperbarui posisi player dan musuh.
        - Memperbarui waktu saat ini.
        - Memperbarui elemen ledakan.
        - Membuat musuh baru.
        - Memperbarui player.
        - Memperbarui musuh.
        - Menghapus elemen objek yang tidak diperlukan.
        - Memeriksa serangan actor.
        - Menampilkan ledakan pada layar.
        """
        self.position_player = (self.player.rect.x, self.player.rect.y) # Mengambil posisi player saat ini
        self.position_enemys = list(map(lambda enemy: (enemy.rect.x, enemy.rect.y), self.enemies)) # List yang menampung posisi dari semua enemy
        self.current_time = pygame.time.get_ticks()
        self.explosions.update()
        self.bullet_explosions.update()
        self.create_enemy()
        self.player.update()
        self.enemy_update()
        self.remove_elemen_obj()
        self.cek_actor_attack()
        self.explosions.draw(self.screen)
        self.bullet_explosions.draw(self.screen)

    # Memperbarui setiap musuh dalam permainan.
    def enemy_update(self):
        """
        Memperbarui setiap musuh dalam permainan.
        """
        for enemy in self.enemies:
            if enemy.enemy_type != "kamikaze":
                enemy.update()
            else:
                enemy.update(self.position_player)

    # Menghapus elemen objek yang sudah tidak terlihat pada layar.
    def remove_elemen_obj(self):
        """
        Menghapus elemen objek yang sudah tidak terlihat pada layar.

        - Menghapus serangan player yang melewati batas atas layar.
        - Menghapus serangan musuh yang melewati batas bawah layar.
        """
        # Memfilter dan hanya menyimpan serangan player yang masih berada di layar
        try:
            for attacks_d in self.player.player_basic_attacks:
                pygame.sprite.Group([attack for attack in attacks_d if attack.rect.y > 0])
        except Exception as e:
            print(e)

        # Memfilter dan hanya menyimpan serangan musuh yang masih berada di layar
        for enemy in self.enemies:
            enemy.enemy_basic_attacks = pygame.sprite.Group(
                [attack for attack in enemy.enemy_basic_attacks if attack.rect.y < self.screen_height]
            )

    # Mengecek dan membuat serangan dasar baik dari player maupun musuh.
    def cek_actor_attack(self):
        """
        Mengecek dan membuat basic attack baik dari player.
        """
        # Memastikan ada musuh sebelum membuat serangan player
        if self.enemies:
            self.player.create_basic_attack_player(AttackActor, self.player,  self.player.last_BasicAttack_time)
            
    # Membuat, menangani, dan menampilkan musuh-musuh dalam permainan.
    def create_enemy(self):
        """
        Membuat, menangani, dan menampilkan musuh-musuh dalam permainan.

        - Memeriksa waktu permainan dan menggambar musuh jika sudah waktunya.
        - Menggambar dan memperbarui tampilan kesehatan musuh.
        - Menangani serangan player terhadap musuh dan menghasilkan efek ledakan jika musuh terkena.
        - Menangani serangan musuh terhadap player dan mengurangi kesehatan player.
        - Menghapus musuh dari layar jika sudah mencapai ujung jalur geraknya.
        """
        for enemy in self.enemies:
            # Mengecek apakah sudah waktunya untuk menggambar musuh
            if self.current_time - self.start_game >= enemy.delay_to_next_path[0]:
                # Menggambar musuh dan memperbarui tampilan kesehatan musuh
                enemy.draw(self.screen)
                enemy.draw_health(enemy.enemy_type)

                # Menangani serangan player terhadap musuh
                try:
                    for attacks in self.player.player_basic_attacks:
                        for attack in attacks:
                            if enemy.health <= 0:
                                # Menangani ledakan dan menghapus musuh jika kesehatan habis
                                self.handle_enemy_death(enemy)
                                if len(self.explosions) < 5:
                                    self.explosions.add(Explosion(x=enemy.rect.x + random.randint(-50, 50), y=enemy.rect.y + random.randint(-50, 50), explosion_images=self.image_explosion))
                            # Menangani serangan player dan efek ledakan
                            if attack.rect.colliderect(enemy.rect):
                                self.handle_attack_collision(enemy, attacks, attack)
                except Exception as e:
                    print(f'Error: {e}')

            # Menangani serangan musuh terhadap player
            self.handle_enemy_attack(enemy)
            
            # Menghapus musuh dari layar jika sudah mencapai ujung jalur geraknya
            if not ( enemy.rect.x <= self.screen_width and enemy.rect.y <= self.screen_height) :
                self.enemies.remove(enemy)
            
    # Mengatasi masalah tabrakan player maupun attack player
    def handle_attack_collision(self, enemy, attacks, attack):
        """Menangani serangan player dan efek ledakan."""
        enemy.health -= self.player.damage
        explosions = self.bullet_explosions_image
        x, y = attack.rect.x, attack.rect.y
        if self.player.type_basicAttack == "type_2":
            self.bullet_explosions.add(Explosion(x=x - 10, y=y, explosion_images=explosions))
            self.bullet_explosions.add(Explosion(x=x + 10, y=y, explosion_images=explosions))
        elif self.player.type_basicAttack == "type_1":
            self.bullet_explosions.add(Explosion(x=x, y=y, explosion_images=explosions))
        attacks.remove(attack)

    # Menangani score player dan juga bagaimana enemy meledak dan di hapus
    def handle_enemy_death(self, enemy):
        """Menangani ledakan dan menghapus musuh jika kesehatan habis."""
        self.player.score += 10
        self.enemies.remove(enemy)

    # Menganani attack dari enemy
    def handle_enemy_attack(self, enemy):
        """Menangani serangan musuh terhadap player."""
        for attack in enemy.enemy_basic_attacks:
            if attack.rect.colliderect(self.player.rect):
                self.player.take_damage(enemy.damage)
                self.bullet_explosions.add(Explosion(x=attack.rect.x - 10, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                enemy.enemy_basic_attacks.remove(attack)

            if enemy.rect.colliderect(self.player.rect):
                for _ in range(random.randint(1, 2)):
                    self.explosions.add(Explosion(x=enemy.rect.x + random.randint(-50, 50), y=enemy.rect.y + random.randint(-50, 50), explosion_images=self.image_explosion))
                self.player.take_damage(enemy.damage)
                self.enemies.remove(enemy)
        
        if enemy.enemy_type == "Boss":
            for special_attack in enemy.special_attack_bos:
                if special_attack.rect.colliderect(self.player.rect):
                    self.player.take_damage(enemy.damage_special_attack)
                    enemy.special_attack_bos.remove(special_attack)


# Kelas untuk merepresentasikan tingkat permainan.
class Level:
    """
    Kelas untuk merepresentasikan tingkat permainan.

    Args:
    - screen_width (int): Lebar layar permainan.
    - screen_height (int): Tinggi layar permainan.

    Attributes:
    - screen_width (int): Lebar layar permainan.
    - screen_height (int): Tinggi layar permainan.

    Methods:
    - generate_lane (self, formula, num_points=150): Menghasilkan jalur berdasarkan formula matematika.
    """
    # initialisasi class level parent
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    # Menghasilkan jalur berdasarkan formula matematika.
    def generate_lane(self, formula, num_points=150):
        """
        Menghasilkan jalur berdasarkan formula matematika.

        Args:
        - formula (function): Fungsi matematika yang mengembalikan nilai y berdasarkan nilai x.
        - num_points (int): Jumlah titik pada jalur.

        Returns:
        - list: List koordinat (x, y) pada jalur.
        """
        x_values = np.linspace(0, self.screen_width + 1000, num_points)
        y_values = formula(x_values)
        lane = list(zip(x_values, y_values))
        return lane

    # Jalur berbentuk parabola
    def quarter_circle(self, center_x, center_y, radius, num_points=100):
        theta = np.linspace(0, np.pi / 2, num_points)
        x = center_x + radius * np.cos(theta)
        y = center_y + radius * np.sin(theta)
        return x, y

    # Lajur lintasan berbentuk huruf l
    def l_shaped_formula(self, x):
        y = np.piecewise(x, [x <= 500, x > 500], [lambda x: 0, lambda x: np.sin((x - 500) * np.pi / 1000) * 500])
        return y


# Kelas untuk merepresentasikan Level 1 dalam permainan.
class Level1(Battle, Level):
    """
        Kelas untuk merepresentasikan Level 1 dalam permainan.

        Args:
        - screen (Surface): Objek layar permainan.
        - screen_height (int): Tinggi layar permainan.
        - screen_width (int): Lebar layar permainan.

        Attributes:
        - stage (dict): Konfigurasi stage Level 1.

        Methods:
        - __init__ (self, screen, screen_height, screen_width): Inisialisasi objek Level 1.
    """
    
    # initialisasi class level 1
    def __init__(self, screen, screen_height, screen_width):
        level_path = "lvl 1"
        next_level = "lvl 2"
        Level.__init__(self, screen_width, screen_height)
        
        # Background level
        path_image_background = "../resources/assets/BG battle/bg 1.png"   
        
        # >>> Rumus matematika yg digunakan untuk menentukan lajur enemy <<< #
        # Parabla
        parabola = lambda x: 0.001 * (x - screen_width) ** 2 + 100
        
        # garis sinus
        sinusoidal = lambda x: 50 * np.sin(0.02 * x) + 150
        
        num_points = 150
        parabola_lane_normal = self.generate_lane(parabola, num_points)
        sinus_lane = self.generate_lane(sinusoidal, num_points)
        
        
        stage = {
            "Stage 1": [
                EnemyType1(screen = screen, path = [(901, 0), (901, 50), (screen_width, 100)], delay = [1800, 20000, 1000]),
                EnemyType1(screen = screen, path = [(800, 0), (800, 100), (screen_width, 150)], delay = [1700, 20000, 1000]),
                EnemyType1(screen = screen, path = [(700, 0), (700, 150), (screen_width, 200)], delay = [1600, 20000, 1500]), 
                EnemyType1(screen = screen, path = [(600, 0), (600, 100), (screen_width, 250)], delay = [1700, 20000, 1000]),
                EnemyType1(screen = screen, path = [(501, 0), (501, 50), (screen_width, 300)], delay = [1800, 20000, 500]),
            ],
            "Stage 2": [
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [100,200,1000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [150,250,1500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [200,300,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [250,350,2500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
            ],
            "Stage 3" : [
                EnemyType1(screen = screen, path = sinus_lane, delay = [100,200,1000]+[80 for _ in range(len(sinus_lane))]),
                EnemyType1(screen = screen, path = sinus_lane, delay = [150,250,2500]+[80 for _ in range(len(sinus_lane))]),
                EnemyType1(screen = screen, path = sinus_lane, delay = [200,300,3000]+[80 for _ in range(len(sinus_lane))]), 
                EnemyType1(screen = screen, path = sinus_lane, delay = [250,350,3500]+[80 for _ in range(len(sinus_lane))]),
                EnemyType1(screen = screen, path = sinus_lane, delay = [300,400,4000]+[80 for _ in range(len(sinus_lane))]),
            ],
            "Stage 4" : [
                EnemyType2(screen = screen, path = [(901, 0), (901, 50)], delay = [1800, 3000]),
                EnemyType2(screen = screen, path = [(800, 0), (800, 100)], delay = [1700, 4000]),
                EnemyType2(screen = screen, path = [(700, 0), (700, 150)], delay = [1600, 4500]), 
                EnemyType2(screen = screen, path = [(600, 0), (600, 100)], delay = [1700, 4000]),
                EnemyType2(screen = screen, path = [(501, 0), (501, 50)], delay = [1800, 3000]),
            ],
            "delay": [1000, 10000, 5000, 3000]
        }
        super().__init__(screen, screen_height, screen_width, path_image_background, stage, level_path, next_level)


# Kelas untuk merepresentasikan Level 2 dalam permainan.
class Level2(Battle, Level):
    """
        Kelas untuk merepresentasikan Level 2 dalam permainan.

        Args:
        - screen (Surface): Objek layar permainan.
        - screen_height (int): Tinggi layar permainan.
        - screen_width (int): Lebar layar permainan.

        Attributes:
        - stage (dict): Konfigurasi stage Level 1.

        Methods:
        - __init__ (self, screen, screen_height, screen_width): Inisialisasi objek Level 1.
        """
        
    # initialisasi class level 2
    def __init__(self, screen, screen_height, screen_width):
        level_path = "lvl 2"
        next_level = "lvl 3"
        Level.__init__(self, screen_width, screen_height)
        
        # Background level
        path_image_background = "../resources/assets/BG battle/bg 1.png"   
        
        # >>> Rumus matematika yg digunakan untuk menentukan lajur enemy <<< #
        # Setengah lingkaran 
        bola_lane = self.quarter_circle(self.screen_height//4, self.screen_width//4, self.screen_height//2)
        j_lane = self.generate_lane(self.l_shaped_formula)
        j_lane = [(_[0],_[1]-200) for _ in j_lane]
        j_lane_left = j_lane.copy()
        
        j_lane_right = [(self.screen_height-_[0],_[1]) for _ in j_lane.copy()]        
        
        stage = {
            "Stage 1" : [
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [1800, 3000]),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [1700, 4000]),
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [1600, 4000]), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [1700, 4000]),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [1800, 3000])
            ],
            "Stage 2": [
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-250,100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=70, health=700),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-330,140),((self.screen_height//2)-330,0)], delay = [100, 800, 25000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-160,140),((self.screen_height//2)-160,0)], delay = [100, 400, 25000, 500]),

                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+250,100),((self.screen_height//2)+250,0)], delay = [100, 600, 25000, 500], size=70, health=700),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+180,140),((self.screen_height//2)+180,0)], delay = [100, 400, 25000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+350,140),((self.screen_height//2)+350,0)], delay = [100, 800, 25000, 500])
            ],
            "Stage 3" : [
                EnemyType1(screen = screen, path = j_lane_left, delay = [0,400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_left, delay = [200,600]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_left, delay = [400,800]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_left, delay = [600,1000]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_left, delay = [800,1200]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_left, delay = [1000,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3),

                EnemyType1(screen = screen, path = j_lane_right, delay = [0,400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_right, delay = [200,600]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_right, delay = [400,800]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_right, delay = [600,1000]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_right, delay = [800,1200]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3),
                
                EnemyType2(screen = screen, path = [(self.screen_height-200, -10), (self.screen_height-200, 150)], delay = [1600, 8000]), 
                EnemyType2(screen = screen, path = [(self.screen_height-300, -10), (self.screen_height-300, 150)], delay = [1600, 8000]), 
                EnemyType2(screen = screen, path = [(200, -10), (200, 150)], delay = [1600, 8000]), 
                EnemyType2(screen = screen, path = [(200, -10), (300, 250)], delay = [1600, 8000])
            ],
            "Stage 4" : [
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=3000),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=60),
                
                EnemyType1(screen = screen, path = j_lane_left, delay = [9000,400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9200,600]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9400,800]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9600,1000]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9800,1200]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10000,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=60),

                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,50),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,30),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,10),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),

                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,50),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,30),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,10),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500])
            ],
            "Stage 5": [
                EnemyType1(screen = screen, path = [(self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),-20)], delay = [600, 20000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(0,0),((self.screen_height//2)-200,60),((self.screen_height//2)-100,-20)], delay = [600, 20000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height,0),((self.screen_height//2)+200,60),((self.screen_height//2)+100,-20)], delay = [600, 20000, 500], size=90, health=2000),
                
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,160),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,160),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType2(screen = screen, path = [(800, -10), (800, 20)], delay = [11700, 9000]),
                EnemyType2(screen = screen, path = [(700, -10), (700, 50)], delay = [11600, 9000]), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 20)], delay = [11700, 9000])
                
            ],
            "Stage 6" : [
                EnemyType1(screen = screen, path = [(0,0), (0,0),((self.screen_height//2-200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=1500),
                EnemyType1(screen = screen, path = [(self.screen_height,0), (self.screen_height,0),((self.screen_height//2+200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=1500),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-400,250),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-300,240),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-200,230),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-100,220),(0,0)], delay = [1000, 25000, 1000]),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+400,250),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+300,240),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+200,230),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+100,220),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000])
            ],
            "Stage 7" : [
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [1800, 3000], size=60, health=150),
                EnemyType2(screen = screen, path = [(800, -10), (800, 50)], delay = [1700, 4000], size=60, health=150),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [1700, 4000], size=60, health=150),
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 4000], size=60, health=150), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [1600, 4000], size=60, health=150), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 4000], size=60, health=150), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [1700, 4000], size=60, health=150),
                EnemyType2(screen = screen, path = [(600, -10), (600, 50)], delay = [1700, 4000], size=60, health=150),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [1800, 3000], size=60, health=150)
            ],
            "delay": [1000, 10000, 10000, 10000, 10000, 10000, 10000]
        }

        super().__init__(screen, screen_height, screen_width, path_image_background, stage, level_path, next_level)
    
    
# Kelas untuk merepresentasikan Level 3 dalam permainan.
class Level3(Battle, Level):
    """
        Kelas untuk merepresentasikan Level 3 dalam permainan.

        Args:
        - screen (Surface): Objek layar permainan.
        - screen_height (int): Tinggi layar permainan.
        - screen_width (int): Lebar layar permainan.

        Attributes:
        - stage (dict): Konfigurasi stage Level 1.

        Methods:
        - __init__ (self, screen, screen_height, screen_width): Inisialisasi objek Level 1.
        """
    
    # initialisasi class level 1
    def __init__(self, screen, screen_height, screen_width):
        level_path = "lvl 3"
        next_level = "lvl 4"
        Level.__init__(self, screen_width, screen_height)
        
        # Background level
        path_image_background = "../resources/assets/BG battle/bg 2.png"
        
        # >>> Rumus matematika yg digunakan untuk menentukan lajur enemy <<< #
        # Setengah lingkaran 
        bola_lane = self.quarter_circle(self.screen_height//4, self.screen_width//4, self.screen_height//2)
        j_lane = self.generate_lane(self.l_shaped_formula)
        j_lane = [(_[0]-200,_[1]-200) for _ in j_lane]
        j_lane_left = j_lane.copy()
        j_lane_right = [(self.screen_height-_[0],_[1]) for _ in j_lane.copy()]         
        
        # Garis Parabola
        parabola = lambda x: 0.001 * (x - screen_width) ** 2 + 100
        
        # garis sinus
        sinusoidal = lambda x: 50 * np.sin(0.02 * x) + 130
        
        # Implementasi dan persiapan lajur musuh
        num_points = 150
        parabola_lane_normal = self.generate_lane(parabola, num_points)
        parabola_lane_reverse = parabola_lane_normal.copy()
        parabola_lane_reverse.reverse()
        
        sinus_lane = self.generate_lane(sinusoidal, num_points)
        
        
        stage = {
            "Stage 1" : [
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2-300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=1500),
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,100),((self.screen_height//2),200),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=1500),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2+300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=1500),
            
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4200,600]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4400,800]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4600,1000]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4800,1200]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,1400]+[100 for _ in range(len(j_lane_left))]+[3000]),
            ],
            "Stage 2": [
                EnemyType1(screen = screen, path = [(0,0), (0,0),((self.screen_height//2-200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height,0), (self.screen_height,0),((self.screen_height//2+200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-400,250),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-300,240),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-200,230),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-100,220),(0,0)], delay = [1000, 25000, 1000]),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+400,250),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+300,240),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+200,230),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+100,220),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000])
            ],
            "Stage 3" : [
                EnemyType2(screen = screen, path = [(901, -10), (1200, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1100, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1000, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 50)], delay = [1700, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(600, -10), (600, 50)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (301, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000]),
            ],
            "Stage 4" : [
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 20000, 500], size=70, health=1000),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 20000, 500]),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [9000,400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [9200,600]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [9400,800]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [9600,1000]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [9800,1200]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [10000,1400]+[70 for _ in range(len(j_lane_right))]+[3000])
            ],
            "Stage 5": [
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=4000),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                
                EnemyType1(screen = screen, path = j_lane_left, delay = [9000,400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9200,600]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9400,800]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9600,1000]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9800,1200]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10000,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),

                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-200,50),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-300,30),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2)-400,10),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),

                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,50),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,30),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,10),((self.screen_height//2)-330,0)], delay = [20000, 800, 20000, 500])
            ],
            "Stage 6" : [
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2200,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2400,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2600,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2800,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_right, delay = [3000,1400]+[70 for _ in range(len(j_lane_right))]+[3000], speed=3, health=80),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),-20)], delay = [600, 25000, 500], size=90, health=3000),
                EnemyType1(screen = screen, path = [(0,0),((self.screen_height//2)-200,60),((self.screen_height//2)-100,-20)], delay = [600, 25000, 500], size=90, health=3000),
                EnemyType1(screen = screen, path = [(self.screen_height,0),((self.screen_height//2)+200,60),((self.screen_height//2)+100,-20)], delay = [600, 25000, 500], size=90, health=3000),
                
                EnemyType1(screen = screen, path = j_lane_left, delay = [9000,400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9200,600]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9400,800]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9600,1000]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [9800,1200]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10000,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10200,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10400,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10600,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10800,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
                EnemyType1(screen = screen, path = j_lane_left, delay = [11000,1400]+[70 for _ in range(len(j_lane_left))]+[3000], speed=3, health=80),
            ],
            "Stage 7" : [
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=5000),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
            ],
            "Stage 8" : [
                EnemyType1(screen = screen, path = sinus_lane, delay = [150,250,2500]+[80 for _ in range(len(sinus_lane))]),
                EnemyType1(screen = screen, path = sinus_lane, delay = [200,300,3000]+[80 for _ in range(len(sinus_lane))]), 
                EnemyType1(screen = screen, path = sinus_lane, delay = [250,350,3500]+[80 for _ in range(len(sinus_lane))]),
                EnemyType1(screen = screen, path = sinus_lane, delay = [300,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [350,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [400,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [450,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [500,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [550,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [600,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [650,400,4000]+[80 for _ in range(len(sinus_lane))]),    
                EnemyType1(screen = screen, path = sinus_lane, delay = [700,400,4000]+[80 for _ in range(len(sinus_lane))]),
                
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2-300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 40000, 500], size=90, health=1500),
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,100),((self.screen_height//2),200),((self.screen_height//2)-250,0)], delay = [100, 600, 40000, 500], size=90, health=1500),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2+300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 40000, 500], size=90, health=1500), 
            ],
            "Stage 9" : [
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [100,200,1000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [150,250,1500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [200,300,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [250,350,2500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_normal)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),

                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_reverse)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=5000),

            ],
            "delay": [1000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
        }

        super().__init__(screen, screen_height, screen_width, path_image_background, stage, level_path, next_level)
    
    
# Kelas untuk merepresentasian Level 4 dalam permainan (melawan bos stage 1)
class Level4(Battle, Level):
    
    # initialisasi class level 1
    def __init__(self, screen, screen_height, screen_width):
        level_path = "lvl 4"
        next_level = "lvl 5"
        Level.__init__(self, screen_width, screen_height)
        
        # Background level
        path_image_background = "../resources/assets/BG battle/bg 2.png"
        
        # >>> Rumus matematika yg digunakan untuk menentukan lajur enemy <<< #
        # Setengah lingkaran 
        bola_lane = self.quarter_circle(self.screen_height//4, self.screen_width//4, self.screen_height//2)
        j_lane = self.generate_lane(self.l_shaped_formula)
        j_lane = [(_[0]-200,_[1]-200) for _ in j_lane]
        j_lane_left = j_lane.copy()
        j_lane_right = [(self.screen_height-_[0],_[1]) for _ in j_lane.copy()]         
        
        # Garis Parabola
        parabola = lambda x: 0.001 * (x - screen_width) ** 2 + 100
        
        # garis sinus
        sinusoidal = lambda x: 50 * np.sin(0.02 * x) + 130
        
        # Implementasi dan persiapan lajur musuh
        num_points = 150
        parabola_lane_normal = self.generate_lane(parabola, num_points)
        parabola_lane_reverse = parabola_lane_normal.copy()
        parabola_lane_reverse.reverse()
        
        sinus_lane = self.generate_lane(sinusoidal, num_points)
        
        
        stage = {
            "Stage 1" : [
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2-300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,100),((self.screen_height//2),200),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2+300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
            
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4200,600]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4400,800]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4600,1000]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4800,1200]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,1400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [100,200,1000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [150,250,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [200,300,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [250,350,2500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_normal)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),

                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_reverse)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
            ],
            "Stage 2": [
                EnemyType1(screen = screen, path = [(0,0), (0,0),((self.screen_height//2-200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height,0), (self.screen_height,0),((self.screen_height//2+200),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-400,250),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-300,240),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-200,230),(0,0)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2-300,0), (self.screen_height//2-100,220),(0,0)], delay = [1000, 25000, 1000]),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+400,250),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+300,240),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+200,230),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                EnemyType1(screen = screen, path = [(self.screen_height//2+300,0), (self.screen_height//2+100,220),(self.screen_height,self.screen_width)], delay = [1000, 25000, 1000]),
                
                EnemyType2(screen = screen, path = [(901, -10), (1200, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1100, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1000, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 50)], delay = [1700, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [1600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(600, -10), (600, 50)], delay = [1700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (301, 50)], delay = [1800, 4000], size=60, health=200, damage=70),
                
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000]),
            ],
            "Stage 3" : [
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=6000),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
            ],
            "Stage 4" : [
                EnemyBoss(screen = screen, 
                    path = [
                        (self.screen_height//2-200, -50), 
                        (self.screen_height//2-200, 20), 
                        (self.screen_height-200, 20),
                        (100, 20),
                        (130, 10),
                        (self.screen_height-230, 10),
                        (self.screen_height//2-200, 20), 
                        (130, 10),
                        (100, 20),
                        (self.screen_height-200, 20)
                        ], 
                    delay = [1000, 23000, 15000, 23000, 20000, 20000, 23000, 15000, 23000, 1000],
                    health=30000),
            
                EnemyType1(screen = screen, path = j_lane_left, delay = [10000,400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10200,600]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10400,800]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10600,1000]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10800,1200]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [10000,1400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20100,200,1000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20150,250,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20200,300,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20250,350,2500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20350,350,3500]+[50 for _ in range(len(parabola_lane_normal)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20350,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [20400,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
            ],
            "delay": [1000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
        }

        super().__init__(screen, screen_height, screen_width, path_image_background, stage, level_path, next_level)


# Kelas untuk merepresentasian Level 5 dalam permainan (melawan bos stage 2)
class Level5(Battle, Level):
    # initialisasi class level 1
    def __init__(self, screen, screen_height, screen_width):
        level_path = "lvl 5"
        next_level = None
        Level.__init__(self, screen_width, screen_height)
        
        # Background level
        path_image_background = "../resources/assets/BG battle/bg 2.png"
        
        # >>> Rumus matematika yg digunakan untuk menentukan lajur enemy <<< #
        # Setengah lingkaran 
        bola_lane = self.quarter_circle(self.screen_height//4, self.screen_width//4, self.screen_height//2)
        j_lane = self.generate_lane(self.l_shaped_formula)
        j_lane = [(_[0]-200,_[1]-200) for _ in j_lane]
        j_lane_left = j_lane.copy()
        j_lane_right = [(self.screen_height-_[0],_[1]) for _ in j_lane.copy()]         
        
        # Garis Parabola
        parabola = lambda x: 0.001 * (x - screen_width) ** 2 + 100
        
        # garis sinus
        sinusoidal = lambda x: 50 * np.sin(0.02 * x) + 130
        
        # Implementasi dan persiapan lajur musuh
        num_points = 150
        parabola_lane_normal = self.generate_lane(parabola, num_points)
        parabola_lane_reverse = parabola_lane_normal.copy()
        parabola_lane_reverse.reverse()
        
        sinus_lane = self.generate_lane(sinusoidal, num_points)
        
        
        stage = {
            "Stage 1" : [
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_reverse)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                
                EnemyType2(screen = screen, path = [(901, -10), (1200, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1100, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (1000, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 50)], delay = [9700, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [9700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [9600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [9600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [9600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [9700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(600, -10), (600, 50)], delay = [9700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (401, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (301, 50)], delay = [9800, 4000], size=60, health=200, damage=70),
            ],
            "Stage 2": [
                EnemyType1(screen = screen, path = j_lane_right, delay = [1000,400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1200,600]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1400,800]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1600,1000]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [1800,1200]+[70 for _ in range(len(j_lane_right))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_right, delay = [2000,1400]+[70 for _ in range(len(j_lane_right))]+[3000]),
                
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,0),((self.screen_height//2),100),((self.screen_height//2),0)], delay = [100, 600, 40000, 500], size=70, health=6000),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+200,140),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+300,120),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+400,100),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+500,80),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2)+600,60),((self.screen_height//2)-330,0)], delay = [100, 800, 40000, 500]),

            ],
            "Stage 3" : [
                EnemyBoss(screen = screen, 
                    path = [
                        (self.screen_height//2-200, -50), 
                        (self.screen_height//2-200, 20), 
                        (self.screen_height-200, 20),
                        (100, 20),
                        (130, 10),
                        (self.screen_height-230, 10),
                        (self.screen_height//2-200, 20), 
                        (130, 10),
                        (100, 20),
                        (self.screen_height-200, 20)
                        ], 
                    delay = [1000, 23000, 15000, 23000, 20000, 20000, 23000, 15000, 23000, 1000],
                    health=40000, delay_next_special_attack=12000, special_attack_active=5000, delay_next_basic_attack=8000, basic_attack_active=7000),
            
                EnemyType1(screen = screen, path = [(0,100), (0,100),((self.screen_height//2-300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height//2,0), (self.screen_height//2,100),((self.screen_height//2),200),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
                EnemyType1(screen = screen, path = [(self.screen_height,100), (self.screen_height,100),((self.screen_height//2+300),100),((self.screen_height//2)-250,0)], delay = [100, 600, 25000, 500], size=90, health=2000),
            
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4200,600]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4400,800]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4600,1000]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4800,1200]+[100 for _ in range(len(j_lane_left))]+[3000]),
                EnemyType1(screen = screen, path = j_lane_left, delay = [4000,1400]+[100 for _ in range(len(j_lane_left))]+[3000]),
                
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [100,200,1000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [150,250,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [200,300,2000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [250,350,2500]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,350,3500]+[50 for _ in range(len(parabola_lane_normal)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [300,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [350,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [400,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [450,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [500,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [550,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_normal, delay = [600,300,3000]+[50 for _ in range(len(parabola_lane_normal)-3)]),

                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10350,350,3500]+[50 for _ in range(len(parabola_lane_reverse)-3)]),    
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10300,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10350,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10400,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10450,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10500,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10550,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                EnemyType1(screen = screen, path = parabola_lane_reverse, delay = [10600,300,3000]+[50 for _ in range(len(parabola_lane_reverse)-3)]),
                
                EnemyType2(screen = screen, path = [(901, -10), (901, 50)], delay = [25800, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 50)], delay = [25700, 4000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(800, -10), (800, 100)], delay = [25700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [25600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 150)], delay = [25600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(700, -10), (700, 100)], delay = [25600, 5000], size=60, health=200, damage=70), 
                EnemyType2(screen = screen, path = [(600, -10), (600, 100)], delay = [25700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(600, -10), (600, 50)], delay = [25700, 5000], size=60, health=200, damage=70),
                EnemyType2(screen = screen, path = [(501, -10), (501, 50)], delay = [25800, 4000], size=60, health=200, damage=70),
            ],
            "delay": [1000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
        }

        super().__init__(screen, screen_height, screen_width, path_image_background, stage, level_path, next_level)
    