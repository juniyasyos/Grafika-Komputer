from .player import Player
from .enemy import EnemyType1, EnemyType2
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
        
        Methods:
        - update (self) : memperbarui objek ledakan.
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
            self.frame +=  1
            
            # Memeriksa apakah sudah mencapai frame terakhir
            if self.frame == len(self.images):
                # Jika ya, menghapus objek ledakan (kill)
                self.kill()
            else:
                # Jika belum, memperbarui gambar dan posisi objek ledakan berdasarkan frame
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center = self.rect.center)


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
        
        Methods:
        - run_battle (self): 
        - enemy_update (self):  
        - remove_elemen_obj (self):  
        - cek_actor_attack (self):  
        - create_enemy (self):  
        """
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.start_game = gp.pygame.time.get_ticks()

        # Elemen global
        self.explosions = gp.pygame.sprite.Group()
        self.image_explosion = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion3/{i+1}.png",size = (50,50), scale = 2) for i in range(30)]
        self.bullet_explosions = gp.pygame.sprite.Group()
        self.bullet_explosions_image = [gp.load_image(f"../resources/assets/Battle/Explotisions/Explosion4/{i+1}.png",size = (15,15), scale = 2) for i in range(25)]
        
        # Membuat objek Player dan elemennya
        self.player = Player(self.screen_width, self.screen_height, screen = self.screen)

        # Membuat objek Enemy dan elemennya
        self.enemies = gp.pygame.sprite.Group()


    def run_battle(self):
        self.position_player = (self.player.rect.x, self.player.rect.y) # Mengambil posisi player saat ini
        self.position_enemys = list(map(lambda enemy: (enemy.rect.x, enemy.rect.y), self.enemies)) # List yang menampung posisi dari semua enemy
        self.current_time = gp.pygame.time.get_ticks()
        self.explosions.update()
        self.bullet_explosions.update()
        self.create_enemy()
        self.player.update()
        self.enemy_update()
        self.remove_elemen_obj()
        self.cek_actor_attack()
        self.explosions.draw(self.screen)
        self.bullet_explosions.draw(self.screen)


    def enemy_update(self):
        """
        Memperbarui setiap musuh dalam permainan.
        """
        for enemy in self.enemies:
            if enemy.enemy_type == "normal":
                enemy.update()
            elif enemy.enemy_type == "kamikaze":
                enemy.update(self.position_player)


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
            # menghapus musuh yang keluar dari layar
            if (0 > enemy.rect.x > self.screen_width) or (0 > enemy.rect.y > self.screen_height):
                enemy.kill()


    def cek_actor_attack(self):
        """
        Mengecek dan membuat serangan dasar baik dari player maupun musuh.
        """
        # Memastikan ada musuh sebelum membuat serangan musuh
        if self.enemies:
            for enemy in self.enemies:
                # Membuat serangan musuh dengan parameter yang sesuai
                if enemy.enemy_type == "normal":
                    enemy.create_basic_attack_enemy(
                        AttackActor, enemy, self.current_time, enemy.last_BasicAttack_time,
                        cooldown_basicAttack = gp.random.randint(5000, 10000),
                        count_all_enemy = len(self.enemies)
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
            if self.current_time - self.start_game >=  enemy.delay_to_next_path[0]:
                
                # Menggambar musuh dan memperbarui tampilan kesehatan musuh
                enemy.draw(self.screen)
                enemy.draw_health()
                enemy_attack = False

                # Menangani serangan player terhadap musuh
                for attacks in self.player.player_basic_attacks:
                    for attack in attacks:
                        if enemy.health <=  0:
                            # Menangani ledakan dan menghapus musuh jika kesehatan habis
                            if enemy in self.enemies: 
                                for jml_explosions in range(gp.random.randint(1, 2)):
                                    self.explosions.add(Explosion(x = enemy.rect.x+gp.random.randint(-50, 50), y = enemy.rect.y+gp.random.randint(-50, 50), explosion_images = self.image_explosion))
                                self.player.score +=  1
                                self.enemies.remove(enemy)

                        # Menangani serangan player dan efek ledakan
                        if attack.rect.colliderect(enemy.rect):
                            enemy.health -=  self.player.damage
                            if self.player.type_basicAttack == "type_2": 
                                self.bullet_explosions.add(Explosion(x = attack.rect.x-10, y = attack.rect.y, explosion_images = self.bullet_explosions_image))
                                self.bullet_explosions.add(Explosion(x = attack.rect.x+10, y = attack.rect.y, explosion_images = self.bullet_explosions_image))
                            elif self.player.type_basicAttack == "type_1":
                                self.bullet_explosions.add(Explosion(x = attack.rect.x, y = attack.rect.y, explosion_images = self.bullet_explosions_image))
                            attacks.remove(attack)

            for attack in enemy.enemy_basic_attacks:
                if attack.rect.colliderect(self.player.rect):
                    self.player.take_damage(enemy.damage)
                    self.bullet_explosions.add(Explosion(x = attack.rect.x-10, y = attack.rect.y, explosion_images = self.bullet_explosions_image))
                    enemy.enemy_basic_attacks.remove(attack)
            
            if enemy.rect.colliderect(self.player.rect):
                for jml_explosions in range(gp.random.randint(1, 2)):
                    self.explosions.add(Explosion(x = enemy.rect.x+gp.random.randint(-50, 50), y = enemy.rect.y+gp.random.randint(-50, 50), explosion_images = self.image_explosion))
                self.player.take_damage(enemy.damage)
                self.enemies.remove(enemy)
                

            # Menghapus musuh dari layar jika sudah mencapai ujung jalur geraknya
            if 0 < enemy.rect.x > self.screen_width or enemy.rect.y > self.screen_height:
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
        self.path_delay =  gp.pygame.time.get_ticks()
        self.next_stage_delay = 0
        # self.path_image_background = {'bg_basic':"../resources/assets/BG battle/star 2.png", 'object':["../resources/assets/BG battle/planet 1.png", "../resources/assets/BG battle/planet 2.png"]}
        self.path_image_background = "../resources/assets/BG battle/bg 1.png"   
        self.kill_player_delay = 0 
        
        num_points = 150
        x_values = gp.np.linspace(0, self.screen_width, num_points)
        y_values = 0.001 * (x_values - self.screen_height) ** 2 + 100
        path_curve = list(zip(x_values, y_values))
        path_curve_normal = path_curve.copy()
        
        path_curve_reverse = path_curve.copy()
        path_curve_reverse.reverse()
        
        
        self.stage = {
            "Stage 1": [
                EnemyType1(screen = self.screen, path = [(901, 0), (901, 50), (self.screen_width, 100)], delay = [1800, 20000, 500], x=None, y=None),
                EnemyType1(screen = self.screen, path = [(800, 0), (800, 100), (self.screen_width, 150)], delay = [1700, 20000, 1000], x=None, y=None),
                EnemyType1(screen = self.screen, path = [(700, 0), (700, 150), (self.screen_width, 200)], delay = [1600, 20000, 1500], x=None, y=None), 
                EnemyType1(screen = self.screen, path = [(600, 0), (600, 100), (self.screen_width, 250)], delay = [1700, 20000, 1000], x=None, y=None),
                EnemyType1(screen = self.screen, path = [(501, 0), (501, 50), (self.screen_width, 300)], delay = [1800, 20000, 500], x=None, y=None),
            ],
            "Stage 2": [
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [100,200,1000]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [150,250,1500]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [200,300,2000]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [250,350,2500]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [300,300,3000]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_normal, delay = [350,350,3500]+[50 for _ in range(len(path_curve_normal)-3)], x=None, y=None),
                
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [100,200,1000]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [150,250,1500]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [200,300,2000]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [250,350,2500]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [300,300,3000]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
                EnemyType1(screen = self.screen, path = path_curve_reverse, delay = [350,350,3500]+[50 for _ in range(len(path_curve_reverse)-3)], x=None, y=None),
            ],
            "Stage 3" : [
                EnemyType2(screen = self.screen, path = [(901, 0), (901, 50)], delay = [1800, 2000], x=None, y=None),
                EnemyType2(screen = self.screen, path = [(800, 0), (800, 100)], delay = [1700, 3000], x=None, y=None),
                EnemyType2(screen = self.screen, path = [(700, 0), (700, 150)], delay = [1600, 4000], x=None, y=None), 
                EnemyType2(screen = self.screen, path = [(600, 0), (600, 100)], delay = [1700, 3000], x=None, y=None),
                EnemyType2(screen = self.screen, path = [(501, 0), (501, 50)], delay = [1800, 2000], x=None, y=None),
            ],
            "delay": [1000, 10000, 3000]
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
                current_time = gp.pygame.time.get_ticks()
                self.kill_player_delay = current_time
                stage_delay = self.stage["delay"][self.stage_index]

                if current_time - self.next_stage_delay >= stage_delay:
                    # Menyiapkan dan memulai stage berikutnya
                    self.stage_index += 1
                    self.enemies = gp.pygame.sprite.Group(*self.stage[f"Stage {self.stage_index}"])
                    self.path_delay = current_time
                    self.next_stage_delay = self.path_delay + self.stage["delay"][self.stage_index - 1]
            elif self.stage_index + 1 == len(self.stage):
                # Eksekusi ketika stage selesai
                current_time = gp.pygame.time.get_ticks()
                finish_delay = 6000  # Delai sebelum player bergerak ke atas setelah stage selesai

                if current_time - self.next_stage_delay >= finish_delay:
                    self.stage_index += 1
            

        # gp.ic(self.stage_index)
        # gp.ic(len(self.stage))
        
        # event in battle
        if self.player.health <= 0:
            current_time = gp.pygame.time.get_ticks()
            finish_delay = 8000  # Delai sebelum player bergerak ke atas setelah stage selesai

            if current_time - self.kill_player_delay >= finish_delay:
                return False
            else:
                self.player.handle_option = False
                self.run_battle()
                self.player.player_basic_attacks.clear()
                self.explosions.add(Explosion(x = self.player.rect.x+gp.random.randint(-30, 30)+50, y = self.player.rect.y+gp.random.randint(-30, 30)+40, explosion_images = self.image_explosion))
            
        elif self.stage_index > len(self.stage):
            return True
        else:
            self.run_battle()
            if self.position_player[1] >= 0 and self.stage_index == len(self.stage):
                self.player.rect.y -= self.player.speed
                self.player.player_win = True
            if self.position_player[1] < 0:
                self.stage_index+=1
            return None



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
        self.next_stage_delay = 0
        self.path_delay = gp.pygame.time.get_ticks()
        self.path_image_background = "../resources/assets/BG battle/bg 2.png"
        self.stage = {
            "Stage 1": [
                EnemyType1(screen = self.screen, path = [(100, 100), (300, 50), (self.player.rect.x, self.player.rect.y)], delay = [1000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 50), (450, 100), (self.screen_width, 100)], delay = [2000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (550, 50), (self.screen_width, 200)], delay = [3000, 30000, 0]),
            ],
            "Stage 2": [
                EnemyType1(screen = self.screen, path = [(300, 50), (400, 50), (self.player.rect.x, self.player.rect.y)], delay = [0, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 50), (500, 50), (self.screen_width, 100)], delay = [2000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (600, 50), (self.screen_width, 200)], delay = [3000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (700, 50), (self.screen_width, 200)], delay = [4000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (800, 50), (self.screen_width, 200)], delay = [5000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (90, 50), (self.screen_width, 200)], delay = [6000, 30000, 0]),
            ],
            "Stage 3": [
                EnemyType1(screen = self.screen, path = [(0, 0), (400, 50), (self.player.rect.x, self.player.rect.y)], delay = [100, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (500, 50), (self.screen_width, 100)], delay = [2000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (600, 50), (self.screen_width, 200)], delay = [3000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (700, 50), (self.screen_width, 200)], delay = [4000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (800, 50), (self.screen_width, 200)], delay = [5000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (900, 50), (self.screen_width, 200)], delay = [6000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (1000, 50), (self.screen_width, 200)], delay = [7000, 30000, 0]),
                EnemyType1(screen = self.screen, path = [(0, 0), (1100, 50), (self.screen_width, 200)], delay = [8000, 30000, 0]),
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
                current_time = gp.pygame.time.get_ticks()
                stage_delay = self.stage["delay"][self.stage_index]

                if current_time - self.next_stage_delay >= stage_delay:
                    # Menyiapkan dan memulai stage berikutnya
                    self.stage_index += 1
                    self.enemies = gp.pygame.sprite.Group(*self.stage[f"Stage {self.stage_index}"])
                    self.path_delay = current_time
                    self.next_stage_delay = self.path_delay + self.stage["delay"][self.stage_index-1]
        self.run_battle()
        
        # event in battle
        if self.player.health <= 0: 
            return False
        elif self.stage_index >= len(self.stage)-1:
            return True
        else:
            return None
