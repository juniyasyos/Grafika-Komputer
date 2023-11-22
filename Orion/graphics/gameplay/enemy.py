import pygame
from icecream import ic
import os
import random
import math
from .. import gameplay as gp
        
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
    def __init__(self, x, y, image, screen, path, delay):
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
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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
        self.basic_attack_image = gp.load_image(image_filename="../resources/assets/Battle/bullet.png", rotation=180, colorkey=(255,255,255),size=(16,24), scale=2)
        self.set_update_enemy = []

    def draw(self, screen):
        """Menampilkan gambar musuh di layar."""
        screen.blit(self.image, self.rect)
    
    def update_basic(self):
        """
        Memperbarui pergerakan musuh sesuai jalur gerak.
        """
        
        # Memeriksa apakah sudah waktunya untuk berpindah ke titik jalur gerak berikutnya
        if pygame.time.get_ticks() - self.last_time >= self.delay_to_next_path[0]:
            
            # Memeriksa apakah masih ada titik jalur gerak berikutnya
            if self.path_index < len(self.path):
                target_x, target_y = self.path[self.path_index]
                dx = target_x - self.x
                dy = target_y - self.y
                
                # Menghitung jarak kuadrat antara posisi musuh dan titik tujuan
                distance = dx * dx + dy * dy

                # Menetapkan toleransi kuadrat untuk menentukan apakah musuh sudah mencapai titik tujuan
                tolerance_squared = 10
                
                # Memeriksa apakah musuh sudah mencapai titik tujuan
                if distance < tolerance_squared:
                    # Memeriksa apakah sudah waktunya untuk berpindah ke titik jalur gerak berikutnya
                    if pygame.time.get_ticks() - self.delay_start_time > self.delay_to_next_path[self.path_index]:
                        self.path_index += 1
                        self.delay_start_time = pygame.time.get_ticks()
                else:
                    # Memperbarui pergerakan musuh menuju titik tujuan
                    self.move_towards(target_x, target_y, self.speed)


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
        if distance != 0:
            delta_x /= distance
            delta_y /= distance
        
        # Menghitung perpindahan berdasarkan arah dan kecepatan
        move_x = delta_x * speed
        move_y = delta_y * speed

        # Memperbarui posisi musuh
        self.x += move_x
        self.y += move_y
        
        # Memperbarui posisi rect (kotak batas) musuh
        self.rect.topleft = (int(self.x), int(self.y))

    
    def draw_health(self):
        """Menampilkan indikator kesehatan musuh di layar."""
        
        # Menampilkan batas indikator kesehatan (warna merah)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.rect.x, self.rect.y + 90, self.rect.width, 5))
        
        # Menghitung lebar indikator kesehatan yang sesuai dengan kesehatan saat ini
        current_health_width = (self.health / self.max_health) * self.rect.width
        
        # Menampilkan indikator kesehatan aktual (warna hijau)
        pygame.draw.rect(self.screen, (0, 255, 0), (self.rect.x, self.rect.y + 90, current_health_width, 5))

    

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
    - create_basic_attack_enemy(self, BasicAttack, enemy, current_time, last_time, cooldown_basicAttack, count_all_enemy):
        Membuat basic attack musuh tipe 1.
    - set_basicAttack_func(self):
        Menetapkan fungsi untuk basic attack musuh tipe 1.
    - update(self):
        Memperbarui status musuh tipe 1.
    """
    def __init__(self, screen, path, delay, x=0, y=0):
        """
        Inisialisasi objek musuh tipe 1.

        Parameters:
        - screen (Surface): Layar game.
        - path (list): Jalur gerak musuh dalam bentuk koordinat.
        - delay (list): Waktu delay sebelum musuh mulai bergerak dan pada setiap titik jalur.
        - x (int): Koordinat x awal musuh.
        - y (int): Koordinat y awal musuh.
        """
        image = gp.load_image("../resources/assets/Battle/NPC.png",size=(50,50), rotation=180, colorkey=(255,255,255))
        super().__init__(x, y, image, screen, path, delay)
        self.enemy_basic_attacks = pygame.sprite.Group()
        self.health = 300
        self.max_health = 300
        self.basic_attack_speed = 6

    def create_basic_attack_enemy(self, BasicAttack, enemy, current_time, last_time, cooldown_basicAttack, count_all_enemy):
        """
        Membuat basic attack musuh tipe 1.

        Parameters:
        - BasicAttack: Kelas basic attack.
        - enemy: Musuh yang membuat basic attack.
        - current_time (int): Waktu sekarang dalam permainan.
        - last_time (int): Waktu terakhir basic attack.
        - cooldown_basicAttack (int): Waktu cooldown basic attack.
        - count_all_enemy (int): Jumlah total musuh dalam permainan.
        """
        
        # Memeriksa apakah sudah waktunya untuk membuat basic attack musuh
        if pygame.time.get_ticks() - self.last_time > self.delay_to_next_path[0] + 2000:
            
            # Memeriksa apakah sudah waktunya untuk menggunakan basic attack berdasarkan cooldown
            if current_time - last_time >= cooldown_basicAttack:
                
                # Membuat basic attack musuh dengan parameter yang sesuai
                self.enemy_basic_attacks.add(
                    BasicAttack(
                        screen=self.screen,
                        actor=enemy, 
                        speed=self.basic_attack_speed,
                        image=self.basic_attack_image, 
                        attack_type="Spesial"
                    )
                )
                
                # Memperbarui waktu terakhir basic attack
                self.last_BasicAttack_time = gp.pygame.time.get_ticks()

    
    def set_basicAttack_func(self):
        """Menetapkan fungsi untuk basic attack musuh tipe 1."""
        
        # Memindahkan basic attack musuh ke bawah sesuai dengan kecepatannya
        for attack in self.enemy_basic_attacks.sprites():
            attack.rect.y += attack.speed
            
            # Menampilkan basic attack musuh di layar
            self.screen.blit(attack.image, (attack.rect.x, attack.rect.y))

    def update(self):
        """Memperbarui status musuh tipe 1."""
        
        # Memanggil fungsi untuk menetapkan fungsi basic attack musuh tipe 1
        self.set_basicAttack_func()
        
        # Memperbarui pergerakan musuh sesuai jalur gerak
        self.update_basic()
        