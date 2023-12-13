import pygame
from icecream import ic
import os
import random
import math
from .. import gameplay as gp

# Inisialisasi objek serangan actor.
class Basic_Attack_Normal_Enemy(pygame.sprite.Sprite):
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
        - rect (Rect): Area persegi panjang yang mengelilingi gambar serangan.
          diatur pada posisi awal aktor.
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
    

# class objeck attack special boss enemy
class Spesial_Attack_Bos(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = random.randint(2, 4)
        self.angle = angle
        self.screen = screen

        # Membuat objek Rect
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Memperbarui objek Rect setiap kali posisi berubah
        self.rect.update(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)


# class global enemy 
class obj_Enemy(pygame.sprite.Sprite):
    """
    Representasi objek musuh dalam permainan.

    Parameters:
    - x (int): Koordinat x awal musuh.
    - y (int): Koordinat y awal musuh.
    - image (Surface): Gambar musuh.
    - screen (Surface): Layar game.
    - path (list): Jalur gerak musuh dalam bentuk titik-titik koordinat.
    - delay (list): Waktu delay sebelum musuh bergerak ke titik berikutnya.

    Attributes:
    - x (int): Koordinat x musuh.
    - y (int): Koordinat y musuh.
    - image (Surface): Gambar musuh.
    - rect (Rect): Area persegi panjang yang mengelilingi gambar musuh.
    - screen (Surface): Layar game.
    - health (int): Kesehatan musuh.
    - max_health (int): Kesehatan maksimal musuh.
    - last_BasicAttack_time (int): Waktu terakhir musuh melakukan basic attack.
    - damage (int): Besar kerusakan yang dapat diberikan musuh.
    - start_time (int): Waktu mulai permainan.
    - last_time (int): Waktu terakhir perubahan jalur gerak musuh.
    - path (list): Jalur gerak musuh dalam bentuk titik-titik koordinat.
    - delay_to_next_path (list): Waktu delay sebelum musuh bergerak ke titik berikutnya.
    - path_index (int): Indeks jalur gerak musuh saat ini.
    - delay_start_time (int): Waktu mulai delay sebelum bergerak ke titik berikutnya.
    - speed (int): Kecepatan pergerakan musuh.
    - basic_attack_speed (int): Kecepatan basic attack musuh.
    - basic_attack_image (Surface): Gambar basic attack musuh.
    - set_update_enemy (list): Daftar metode pembaruan khusus musuh.

    Methods:
    - draw(self, screen): Menampilkan gambar musuh di layar.
    - update_basic(self): Memperbarui posisi musuh dengan jalur gerak.
    - move_towards(self, target_x, target_y, speed): Menggerakkan musuh ke arah titik tertentu dengan kecepatan tertentu.
    - draw_health(self): Menampilkan indikator kesehatan musuh di layar.
    """
    def __init__(self, image, screen, path, delay, x=None, y=None):
        """
        Inisialisasi objek musuh.

        Parameters:
        - x (int): Koordinat x awal musuh.
        - y (int): Koordinat y awal musuh.
        - image (Surface): Gambar musuh.
        - screen (Surface): Layar game.
        - path (list): Jalur gerak musuh dalam bentuk titik-titik koordinat.
        - delay (list): Waktu delay sebelum musuh bergerak ke titik berikutnya.
        """
        super().__init__()
        self.x = x
        self.y = y
        if self.x == None:
            self.x = path[0][0]
            self.y = path[0][1]
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.screen = screen
        self.health = 150
        self.max_health = 150
        self.last_BasicAttack_time = 0
        self.damage = 50
        self.start_time = 0
        self.last_time = pygame.time.get_ticks()
        self.path = path
        self.delay_to_next_path = delay
        self.path_index = 0
        self.delay_start_time = 0
        self.speed = 10
        self.basic_attack_speed = 10
        self.basic_attack_image = gp.load_image(image_filename = "../resources/assets/Battle/Laser Sprites/02.png", rotation = 180, colorkey = (255,255,255),size = (16,24), scale = 4)
        self.set_update_enemy = []

    def draw(self, screen):
        """Menampilkan gambar musuh di layar."""
        screen.blit(self.image, self.rect.topleft)
    
    def update_basic(self, enemy_type=None):
        """
        Memperbarui pergerakan musuh sesuai jalur gerak.
        """
        
        # Memeriksa apakah sudah waktunya untuk berpindah ke titik jalur gerak berikutnya
        if pygame.time.get_ticks() - self.last_time >=  self.delay_to_next_path[0]:
            
            # Memeriksa apakah masih ada titik jalur gerak berikutnya
            if self.path_index < len(self.path):
                target_x, target_y = self.path[self.path_index]
                dx = target_x - self.x
                dy = target_y - self.y
                
                # Menghitung jarak kuadrat antara posisi musuh dan titik tujuan
                distance = dx * dx + dy * dy

                # Menetapkan toleransi kuadrat untuk menentukan apakah musuh sudah mencapai titik tujuan
                tolerance_squared = 15
                
                # Memeriksa apakah musuh sudah mencapai titik tujuan
                if distance < tolerance_squared:
                    # Memeriksa apakah sudah waktunya untuk berpindah ke titik jalur gerak berikutnya
                    if pygame.time.get_ticks() - self.delay_start_time > self.delay_to_next_path[self.path_index]:
                        # self.set_angle(target_x, target_y)
                        self.path_index +=  1
                        self.delay_start_time = pygame.time.get_ticks()
                else:
                    # Memperbarui pergerakan musuh menuju titik tujuan
                    self.move_towards(target_x, target_y, self.speed)
            
            else:
                if self.enemy_type == "normal":
                    self.kill()
                elif self.enemy_type == "Boss":
                    self.path_index = 1
                else: 
                    return True

    def move_towards(self, target_x, target_y, speed):
        """
        Menggerakkan musuh menuju titik target dengan kecepatan tertentu.

        Parameters:
        - target_x (int): Koordinat x titik target.
        - target_y (int): Koordinat y titik target.
        - speed (int): Kecepatan pergerakan musuh.
        """
        # Menghitung selisih antara posisi musuh dan titik target
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        
        # Menghitung jarak antara musuh dan titik target
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        
        # Memastikan tidak ada pembagian dengan nol
        if distance !=  0:
            delta_x /=  distance
            delta_y /=  distance
        
        # Menghitung perpindahan berdasarkan arah dan kecepatan
        move_x = delta_x * speed
        move_y = delta_y * speed

        # Memperbarui posisi musuh
        self.x +=  move_x
        self.y +=  move_y
        
        # Memperbarui posisi rect (kotak batas) musuh
        self.rect.topleft = (int(self.x), int(self.y))

    def draw_health(self, type_enemy="normal"):
        """Menampilkan indikator kesehatan musuh di layar."""
        
        margin = 250 if type_enemy == "Boss" else 90
            
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y + margin, self.rect.width, 5))
    
        # Menghitung lebar indikator kesehatan yang sesuai dengan kesehatan saat ini
        current_health_width = (self.health / self.max_health) * self.rect.width
            
        # Menampilkan indikator kesehatan aktual (warna hijau)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y + margin, current_health_width, 5))


# class type enemy normal
class EnemyType1(obj_Enemy):
    """
    Representasi objek musuh tipe 1 dalam permainan.

    Parameters:
    - screen (Surface): Layar game.
    - path (list): Jalur gerak musuh dalam bentuk koordinat.
    - delay (list): Waktu delay sebelum musuh mulai bergerak dan pada setiap titik jalur.
    - x (int): Koordinat x awal musuh.
    - y (int): Koordinat y awal musuh.

    Attributes:
    - enemy_basic_attacks (Group): Grup basic attack musuh.
    - health (int): Kesehatan musuh tipe 1.
    - max_health (int): Kesehatan maksimum musuh tipe 1.
    - basic_attack_speed (int): Kecepatan basic attack musuh tipe 1.

    Methods:
    - create_basic_attack_enemy(self, BasicAttack, enemy, current_time, last_time, cooldown_basicAttack):
        Membuat basic attack musuh tipe 1.
    - set_basicAttack_func(self):
        Menetapkan fungsi untuk basic attack musuh tipe 1.
    - update(self):
        Memperbarui status musuh tipe 1.
    """
    def __init__(self, screen, path, delay, x = None, y = None, speed = 5, size=40, health=300, damage=None):
        """
        Inisialisasi objek musuh tipe 1.

        Parameters:
        - screen (Surface): Layar game.
        - path (list): Jalur gerak musuh dalam bentuk koordinat.
        - delay (list): Waktu delay sebelum musuh mulai bergerak dan pada setiap titik jalur.
        - x (int): Koordinat x awal musuh.
        - y (int): Koordinat y awal musuh.
        """
        image = gp.load_image("../resources/assets/Battle/NPC.png",size = (size,size), rotation = 180, colorkey = (255,255,255))
        
        self.enemy_type = "normal"
        super().__init__(image, screen, path, delay, x=x, y=y)
        self.enemy_basic_attacks = pygame.sprite.Group()
        self.health = health
        self.max_health = health
        self.basic_attack_speed = 5
        self.speed = speed
        if damage != None:
            self.damage = damage
        
    def create_basic_attack_enemy(self, current_time, last_time, cooldown_basicAttack):
        """
        Membuat basic attack musuh tipe 1.

        Parameters:
        - BasicAttack: Kelas basic attack.
        - enemy: Musuh yang membuat basic attack.
        - current_time (int): Waktu sekarang dalam permainan.
        - last_time (int): Waktu terakhir basic attack.
        - cooldown_basicAttack (int): Waktu cooldown basic attack.
        """
        
        # Memeriksa apakah sudah waktunya untuk membuat basic attack musuh
        if pygame.time.get_ticks() - self.last_time > self.delay_to_next_path[0]:
            
            # Memeriksa apakah sudah waktunya untuk menggunakan basic attack berdasarkan cooldown
            if current_time - last_time >=  cooldown_basicAttack:
                
                # Membuat basic attack musuh dengan parameter yang sesuai
                self.enemy_basic_attacks.add(
                    Basic_Attack_Normal_Enemy(
                        screen = self.screen,
                        actor = self, 
                        speed = self.basic_attack_speed,
                        image = self.basic_attack_image, 
                        attack_type = "Spesial"
                    )
                )
                
                # Memperbarui waktu terakhir basic attack
                self.last_BasicAttack_time = pygame.time.get_ticks()
    
    def set_basicAttack_func(self):
        """Menetapkan fungsi untuk basic attack musuh tipe 1."""
        
        # Memindahkan basic attack musuh ke bawah sesuai dengan kecepatannya
        for attack in self.enemy_basic_attacks.sprites():
            attack.rect.y +=  attack.speed
            
            # Menampilkan basic attack musuh di layar
            self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))

    def update(self):
        """Memperbarui status musuh tipe 1."""
        
        self.create_basic_attack_enemy(
            pygame.time.get_ticks(), self.last_BasicAttack_time,
            cooldown_basicAttack = random.randint(3000, 7000))
        
        # Memanggil fungsi untuk menetapkan fungsi basic attack musuh tipe 1
        self.set_basicAttack_func()
        
        # Memperbarui pergerakan musuh sesuai jalur gerak
        self.update_basic()
    
    
# class type enemy kamikaze
class EnemyType2(obj_Enemy):
    def __init__(self, screen, path, delay,x = None, y = None, speed = 6, size=40, health=100, damage=100):
        """
        Inisialisasi objek musuh tipe 2.

        Parameters:
        - screen (Surface): Layar game.
        - path (list): Jalur gerak musuh dalam bentuk koordinat.
        - delay (list): Waktu delay sebelum musuh mulai bergerak dan pada setiap titik jalur.
        - x (int): Koordinat x awal musuh.
        - y (int): Koordinat y awal musuh.
        """
        image = gp.load_image("../resources/assets/Battle/NPC.png", size=(20, 20), rotation=180, colorkey=(255, 255, 255))
        self.enemy_type = "kamikaze"
        super().__init__(image, screen, path, delay, x=x, y=y)
        self.enemy_basic_attacks = pygame.sprite.Group()
        self.health = health
        self.max_health = health
        self.speed = speed
        self.damage = damage
        
    def kamikaze(self, pos_player):
        """
        Metode untuk mengimplementasikan enemy kamikaze dengan konsep Gerak Lurus Berubah Beraturan (GLBB).

        Parameters:
        - pos_player (tuple): Koordinat pemain (x, y).
        """
        target_x, target_y = pos_player
        if (target_x, target_y) != (self.rect.x, self.rect.y):
            try:
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery

                # Normalisasi vektor
                magnitude = (dx ** 2 + dy ** 2) ** 0.5
                normalized_dx = dx / magnitude
                normalized_dy = dy / magnitude
                

                # Perbarui posisi berdasarkan kecepatan
                self.rect.x += int(self.speed * normalized_dx)
                self.rect.y += int(self.speed * normalized_dy)
            except Exception:
                self.kill()
        else:
            self.kill()

    def update(self, pos_player):
        """
        Metode untuk memperbarui posisi musuh.

        Parameters:
        - pos_player (tuple): Koordinat pemain (x, y).
        - last_move (bool): Status pergerakan terakhir pemain.
        """
        endmove = self.update_basic(enemy_type="kamikaze")

        if endmove:
            self.kamikaze(pos_player=pos_player)


# class untuk bas musuh
class EnemyBoss(obj_Enemy):
    def __init__(self, screen, path, delay, x = None, y = None, speed = 1, size=260, health=300, damage=100, basic_attack_speed=5,delay_next_special_attack = 5000, special_attack_active = 3000, delay_next_basic_attack = 10000,basic_attack_active = 5000):
        """
        Inisialisasi objek musuh tipe 1.

        Parameters:
        - screen (Surface): Layar game.
        - path (list): Jalur gerak musuh dalam bentuk koordinat.
        - delay (list): Waktu delay sebelum musuh mulai bergerak dan pada setiap titik jalur.
        - x (int): Koordinat x awal musuh.
        - y (int): Koordinat y awal musuh.
        """
        image = gp.load_image("../resources/assets/Battle/BOSS.png",size = (size,size), rotation = 180, colorkey = (255,255,255))
        
        self.enemy_type = "Boss"
        super().__init__(image, screen, path, delay, x=x, y=y)
        self.enemy_basic_attacks = pygame.sprite.Group()
        self.health = health
        self.max_health = health
        self.basic_attack_speed = basic_attack_speed
        self.speed = speed
        self.damage = damage
        self.damage_special_attack = 40
        self.basic_attack_action = False
        self.special_attack_action = False
        self.special_attack_speed = 5
        self.delay_next_special_attack = delay_next_special_attack
        self.special_attack_active = special_attack_active
        self.delay_next_basic_attack = delay_next_basic_attack
        self.basic_attack_active = basic_attack_active
        self.special_attack_bos = pygame.sprite.Group()

        
    def create_basic_attack_enemy(self, current_time):
        """
        Membuat basic attack musuh tipe 1.

        Parameters:
        - BasicAttack: Kelas basic attack.
        - enemy: Musuh yang membuat basic attack.
        - current_time (int): Waktu sekarang dalam permainan.
        - last_time (int): Waktu terakhir basic attack.
        - cooldown_basicAttack (int): Waktu cooldown basic attack.
        """
        
        # Memeriksa apakah sudah waktunya untuk membuat basic attack musuh
        if pygame.time.get_ticks() - self.last_time > self.delay_to_next_path[0] and self.basic_attack_action:
            
            # Memeriksa apakah sudah waktunya untuk menggunakan basic attack berdasarkan cooldown
            if current_time - self.last_BasicAttack_time >=  500:
                
                # Membuat basic attack musuh dengan parameter yang sesuai
                self.enemy_basic_attacks.add(
                    Basic_Attack_Normal_Enemy(
                        screen = self.screen,
                        actor = self, 
                        speed = self.basic_attack_speed,
                        image = self.basic_attack_image, 
                        attack_type = "Spesial"
                    )
                )
                
                # Memperbarui waktu terakhir basic attack
                self.last_BasicAttack_time = pygame.time.get_ticks()
    
    
    def create_special_attack(self, current_time):
        # Membuat serangan khusus bos
        if self.special_attack_action:
            self.special_attack_bos.add(
                Spesial_Attack_Bos(
                    x=self.rect.centerx+30-(random.randint(10,30)),
                    y=self.rect.centery-80,
                    angle=random.uniform(0, 2 * math.pi),
                    screen=self.screen
                )
            )


    def set_special_attack_func(self):
        # Memindahkan serangan khusus bos dan menampilkannya di layar
        for attack in self.special_attack_bos.sprites():
            attack.move()
            attack.draw()
    
    
    def set_basicAttack_func(self):
        """Menetapkan fungsi untuk basic attack musuh tipe 1."""
        
        # Memindahkan basic attack musuh ke bawah sesuai dengan kecepatannya
        for attack in self.enemy_basic_attacks.sprites():
            attack.rect.y +=  attack.speed
            
            # Menampilkan basic attack musuh di layar
            self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))
    
    
    def update_special_attack_action(self, current_time):
        if current_time - self.last_time >= self.delay_next_special_attack:
            # Aktifkan serangan khusus pada waktu tertentu
            self.special_attack_action = True

        if current_time - self.last_time >= self.delay_next_special_attack + self.special_attack_active:
            # Nonaktifkan serangan khusus setelah beberapa saat
            self.special_attack_action = False
            self.last_time = current_time
            
            
    def update_basic_attack_action(self, current_time):
        if current_time - self.last_time >= self.delay_next_basic_attack:
            # Lakukan sesuatu ketika waktu tertentu tercapai, misalnya aktifkan serangan dasar
            self.basic_attack_action = True

        # Cek apakah serangan dasar musuh harus dinonaktifkan
        if current_time - self.last_time >= self.delay_next_basic_attack + self.basic_attack_active:
            self.basic_attack_action = False
            self.last_time = current_time


    def update(self):
        """Memperbarui status musuh tipe 1."""
        
        current_time = pygame.time.get_ticks()
        
        # Mengecek apakah sudah waktunya basic attack active atau belum
        self.update_basic_attack_action(current_time)
        
        # Membuat basic attack bos 
        self.create_basic_attack_enemy(current_time)
        
        # Memanggil fungsi untuk menetapkan fungsi basic attack musuh tipe 1
        self.set_basicAttack_func()
        
        # Memperbarui pergerakan musuh sesuai jalur gerak
        self.update_basic(enemy_type=self.enemy_type)
        
        # Panggil metode untuk membuat dan mengatur serangan khusus
        self.create_special_attack(current_time)
        self.set_special_attack_func()
        self.update_special_attack_action(current_time)

    
            