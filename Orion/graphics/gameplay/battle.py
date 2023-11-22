from .player import Player
from .enemy import obj_Enemy, EnemyType1
from .. import gameplay as gp

class Explosion(gp.pygame.sprite.Sprite):
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
        """
        
        super().__init__()
        self.images = explosion_images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = gp.pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        """
        Memperbarui objek ledakan pada setiap frame.
        Jika sudah mencapai frame terakhir, objek akan dihapus (kill).
        Pembaruan frame terjadi berdasarkan kecepatan frame_rate.
        """
        
        # Mendapatkan waktu sekarang dalam milidetik
        now = gp.pygame.time.get_ticks()
        
        # Memeriksa apakah sudah waktunya untuk memperbarui frame ledakan
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            
            # Memeriksa apakah sudah mencapai frame terakhir
            if self.frame == len(self.images):
                # Jika ya, menghapus objek ledakan (kill)
                self.kill()
            else:
                # Jika belum, memperbarui gambar dan posisi objek ledakan berdasarkan frame
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center=self.rect.center)


class AttackActor(gp.pygame.sprite.Sprite):
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
        """
    def __init__(self, screen, actor, speed, image, attack_type="basic", func=None):
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

    def update_rocket(self):
        """
        Metode pembaruan khusus untuk serangan roket.
        (Jika diperlukan implementasi khusus, ditambahkan di sini.)
        """
        pass

    def update_laser(self):
        """
        Metode pembaruan khusus untuk serangan laser.
        (Jika diperlukan implementasi khusus, ditambahkan di sini.)
        """
        pass

class Battle:
    def __init__(self, screen, screen_width, screen_height):
        """
        Inisialisasi objek pertempuran.

        Parameters:
        - screen (Surface): Layar game.
        - screen_width (int): Lebar layar game.
        - screen_height (int): Tinggi layar game.

        Attributes:
        - screen (Surface): Layar game.
        - screen_width (int): Lebar layar game.
        - screen_height (int): Tinggi layar game.
        - start_game (int): Waktu mulai permainan.
        - player (Player): Objek player.
        - enemies (Group): Grup objek musuh.
        - explosions (Group): Grup objek ledakan.
        - image_explosion (list): Daftar gambar ledakan.
        - bullet_explosions (Group): Grup objek ledakan peluru.
        - bullet_explosions_image (list): Daftar gambar ledakan peluru.
        """
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.start_game = gp.pygame.time.get_ticks()

        # Elemen global
        self.explosions = gp.pygame.sprite.Group()
        self.image_explosion = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion3/{i+1}.png",size=(50,50), scale=2) for i in range(30)]
        self.bullet_explosions = gp.pygame.sprite.Group()
        self.bullet_explosions_image = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion4/{i+1}.png",size=(15,15), scale=2) for i in range(25)]
        
        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)

        # Membuat objek Enemy dan elemennya
        self.enemies = gp.pygame.sprite.Group()

    def run_battle(self):
        self.current_time = gp.pygame.time.get_ticks()
        self.explosions.update()
        self.bullet_explosions.update()
        self.create_enemy()
        self.player.update()
        self.enemy_update()
        self.remove_elemen_obj()
        self.cek_basic_attack()
        self.explosions.draw(self.screen)
        self.bullet_explosions.draw(self.screen)

    def enemy_update(self):
        """
        Memperbarui setiap musuh dalam permainan.
        """
        for enemy in self.enemies:
            enemy.update()

    def remove_elemen_obj(self):
        """
        Menghapus elemen objek yang sudah tidak terlihat pada layar.

        - Menghapus serangan player yang melewati batas atas layar.
        - Menghapus serangan musuh yang melewati batas bawah layar.
        """
        # Memfilter dan hanya menyimpan serangan player yang masih berada di layar
        for attacks_d in self.player.player_basic_attacks:
            gp.pygame.sprite.Group([attack for attack in attacks_d if attack.rect.y > 0])

        # Memfilter dan hanya menyimpan serangan musuh yang masih berada di layar
        for enemy in self.enemies:
            enemy.enemy_basic_attacks = gp.pygame.sprite.Group(
                [attack for attack in enemy.enemy_basic_attacks if attack.rect.y < self.screen_height]
            )


    def cek_basic_attack(self):
        """
        Mengecek dan membuat serangan dasar baik dari player maupun musuh.
        """
        # Memastikan ada musuh sebelum membuat serangan musuh
        if self.enemies:
            for enemy in self.enemies:
                # Membuat serangan musuh dengan parameter yang sesuai
                enemy.create_basic_attack_enemy(
                    AttackActor, enemy, self.current_time, enemy.last_BasicAttack_time,
                    cooldown_basicAttack=gp.random.randint(2000, 5000),
                    count_all_enemy=len(self.enemies)
                )
            
            # Membuat serangan player dengan parameter yang sesuai
            self.player.create_basic_attack_player(AttackActor, self.player,  self.player.last_BasicAttack_time)


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
                enemy.draw_health()
                enemy_attack = False

                # Menangani serangan player terhadap musuh
                for attacks in self.player.player_basic_attacks:
                    for attack in attacks:
                        if enemy.health <= 0:
                            # Menangani ledakan dan menghapus musuh jika kesehatan habis
                            if enemy in self.enemies: 
                                for jml_explosions in range(gp.random.randint(1, 2)):
                                    self.explosions.add(Explosion(x=enemy.rect.x+gp.random.randint(-50, 50), y=enemy.rect.y+gp.random.randint(-50, 50), explosion_images=self.image_explosion))
                                self.player.score += 1
                                self.enemies.remove(enemy)

                        # Menangani serangan player dan efek ledakan
                        if attack.rect.colliderect(enemy.rect):
                            enemy.health -= self.player.damage
                            if self.player.type_basicAttack == "type_2": 
                                self.bullet_explosions.add(Explosion(x=attack.rect.x-10, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                                self.bullet_explosions.add(Explosion(x=attack.rect.x+10, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                            elif self.player.type_basicAttack == "type_1":
                                self.bullet_explosions.add(Explosion(x=attack.rect.x, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                            attacks.remove(attack)

            # Menangani serangan musuh terhadap player dan mengurangi kesehatan player
            for enemy in self.enemies:
                for attack in enemy.enemy_basic_attacks:
                    if attack.rect.colliderect(self.player.rect):
                        self.player.take_damage(enemy.damage)
                        self.bullet_explosions.add(Explosion(x=attack.rect.x-10, y=attack.rect.y, explosion_images=self.bullet_explosions_image))
                        enemy.enemy_basic_attacks.remove(attack)

                # Menghapus musuh dari layar jika sudah mencapai ujung jalur geraknya
                if enemy.path_index > len(enemy.path):
                    self.enemies.remove(enemy)



class Level1(Battle):
    """
    Representasi level pertama dalam permainan.

    Attributes:
    - stage_index (int): Indeks stage saat ini.
    - stage_delay (int): Waktu delay antar stage.
    - stage (dict): Konfigurasi stage dan musuh-musuhnya.

    Methods:
    - __init__(self, screen, screen_height, screen_width): Inisialisasi objek Level1.
    - run(self): Menjalankan level pertama.
    """

    def __init__(self, screen, screen_height, screen_width):
        """
        Inisialisasi objek Level1.

        Parameters:
        - screen (Surface): Layar game.
        - screen_height (int): Tinggi layar game.
        - screen_width (int): Lebar layar game.

        Attributes:
        - stage_index (int): Indeks stage saat ini.
        - stage_delay (int): Waktu delay antar stage.
        - stage (dict): Konfigurasi stage dan musuh-musuhnya.
        """
        super().__init__(screen, screen_height, screen_width)
        self.stage_index = 0
        self.stage_delay =  gp.pygame.time.get_ticks()
        self.stage = {
            "Stage 1": [
                EnemyType1(screen=self.screen, path=[(100, 100), (300, 50), (self.player.rect.x, self.player.rect.y)], delay=[1000, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 50), (450, 100), (self.screen_width, 100)], delay=[1500, 35000, 0]),
                EnemyType1(screen=self.screen, path=[(0, 0), (550, 50), (self.screen_width, 200)], delay=[2000, 35000, 0]),
            ],
            "delay": [0, 9000, 10000]
        }

    def run(self):
        """
        Menjalankan level pertama.

        - Memeriksa apakah musuh dalam layar sudah habis.
        - Jika sudah, memeriksa apakah masih ada stage berikutnya untuk dijalankan.
        - Jika iya, menyiapkan dan memulai stage berikutnya.
        """
        
        # Memeriksa apakah musuh dalam layar sudah habis
        if len(self.enemies) == 0:
            # Memeriksa apakah masih ada stage berikutnya untuk dijalankan
            if self.stage_index + 1 < len(self.stage):
                # Memeriksa apakah sudah waktunya untuk memulai stage berikutnya
                if gp.pygame.time.get_ticks() - self.stage_delay >= self.stage["delay"][self.stage_index]:
                    # Menyiapkan dan memulai stage berikutnya
                    self.stage_index += 1
                    self.enemies = gp.pygame.sprite.Group(self.stage[f"Stage {self.stage_index}"])
                    self.stage_delay = gp.pygame.time.get_ticks()
                    
        # Menjalankan pertarungan
        self.run_battle()



# Level 2
class Level2(Battle):
    """
    Representasi level kedua dalam permainan.

    Attributes:
    - stage_index (int): Indeks stage saat ini.
    - stage_delay (int): Waktu delay antar stage.
    - stage (dict): Konfigurasi stage dan musuh-musuhnya.

    Methods:
    - __init__(self, screen, screen_height, screen_width): Inisialisasi objek Level1.
    - run(self): Menjalankan level pertama.
    """
    def __init__(self, screen, screen_height, screen_width):
        """
        Inisialisasi objek Level1.

        Parameters:
        - screen (Surface): Layar game.
        - screen_height (int): Tinggi layar game.
        - screen_width (int): Lebar layar game.

        Attributes:
        - stage_index (int): Indeks stage saat ini.
        - stage_delay (int): Waktu delay antar stage.
        - stage (dict): Konfigurasi stage dan musuh-musuhnya.
        """
        super().__init__(screen, screen_height, screen_width)
        self.stage_index = 0
        self.stage_delay = pygame.time.get_ticks()
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
            "delay": [0, 8000, 9000]  
        }

    def run(self):
        """
        Menjalankan level kedua.

        - Memeriksa apakah musuh dalam layar sudah habis.
        - Jika sudah, memeriksa apakah masih ada stage berikutnya untuk dijalankan.
        - Jika iya, menyiapkan dan memulai stage berikutnya.
        """
        
        # Memeriksa apakah musuh dalam layar sudah habis
        if len(self.enemies) == 0:
            # Memeriksa apakah masih ada stage berikutnya untuk dijalankan
            if self.stage_index + 1 < len(self.stage):
                # Memeriksa apakah sudah waktunya untuk memulai stage berikutnya
                if gp.pygame.time.get_ticks() - self.stage_delay >= self.stage["delay"][self.stage_index]:
                    # Menyiapkan dan memulai stage berikutnya
                    self.stage_index += 1
                    self.enemies = gp.pygame.sprite.Group(self.stage[f"Stage {self.stage_index}"])
                    self.stage_delay = gp.pygame.time.get_ticks()
                    
        # Menjalankan pertarungan
        self.run_battle()
