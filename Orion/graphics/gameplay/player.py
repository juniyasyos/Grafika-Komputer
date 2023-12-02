from .. import gameplay as gp

class Player:
    """
    Representasi objek player dalam permainan.

    Parameters:
    - screen_width (int): Lebar layar game.
    - screen_height (int): Tinggi layar game.
    - screen (Surface): Layar game.

    Attributes:
    - screen (Surface): Layar game.
    - screen_width (int): Lebar layar game.
    - screen_height (int): Tinggi layar game.
    - image (Surface): Gambar player.
    - image_rocket (Surface): Gambar roket.
    - rect (Rect): Area persegi panjang yang mengelilingi gambar player.
    - font (Font): Objek font untuk menampilkan teks.
    - speed (int): Kecepatan pergerakan player.
    - health (int): Kesehatan player.
    - max_health (int): Kesehatan maksimum player.
    - score (int): Skor player.
    - damage (int): Jumlah kerusakan yang diakibatkan serangan player.
    - last_BasicAttack_time (int): Waktu terakhir basic attack player.
    - shield (int): Pelindung player.
    - max_shield (int): Pelindung maksimum player.
    - delay_basicAttack (int): Waktu jeda antar basic attack.
    - regen_hp (float): Tingkat regenerasi kesehatan player.
    - type_basicAttack (str): Jenis basic attack player ("type_1" atau "type_2").
    - basic_attack_speed (int): Kecepatan basic attack player.
    - player_basic_attacks_type1 (list): Daftar grup basic attack tipe 1.
    - player_basic_attacks_type2 (list): Daftar grup basic attack tipe 2.
    - available_basic_attacks (list): Daftar basic attack yang belum digunakan.
    - basic_attack_path (Surface): Gambar jalur basic attack.
    - skills (dict): Daftar skill player beserta informasi cooldown dan status aktif.
    - current_time (int): Waktu sekarang dalam permainan.

    Methods:
    - update(self): Memperbarui status player.
    - handle_events(self): Menangani input pengguna untuk menggerakkan player dan menggunakan skill.
    - skill_use(self): Menggunakan dan memproses efek skill player.
    - take_damage(self, damage=10): Mengurangi kesehatan atau pelindung player berdasarkan jumlah kerusakan.
    - draw_health_bar(self): Menampilkan indikator kesehatan dan pelindung player di layar.
    - draw_score(self): Menampilkan skor player di layar.
    - create_basic_attack_player(self, BasicAttack, player, last_time): Membuat basic attack player.
    - draw_icon_skill(self): Menampilkan ikon dan cooldown skill di layar.
    - set_basicAttack_func(self): Menetapkan fungsi untuk menampilkan basic attack player di layar.
    """
    def __init__(self, screen_width, screen_height, screen):
        """
        Inisialisasi objek player.

        Parameters:
        - screen_width (int): Lebar layar game.
        - screen_height (int): Tinggi layar game.
        - screen (Surface): Layar game.
        """
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
        self.speed = 10
        self.health = 200
        self.max_health = 200
        self.score = 0
        self.damage = 24
        self.last_BasicAttack_time = 0
        self.last_RocketAttack_time = 0
        self.shield = 50
        self.max_shield = 50
        self.delay_basicAttack = 200
        self.delay_rocketAttack = 200
        self.regen_hp = 0.004
        self.type_basicAttack = "type_1"
        self.basic_attack_speed = 15
        self.player_rocket_attacks = gp.pygame.sprite.Group()
        self.player_basic_attacks_type1 = [gp.pygame.sprite.Group() for i in range(1)]
        self.player_basic_attacks_type2 = [gp.pygame.sprite.Group() for i in range(2)]
        self.available_basic_attacks = []
        self.player_win = False
        self.handle_option = True
        self.basic_attack_path = gp.load_image("../resources/assets/Battle/Laser Sprites/11.png", scale=3)
        self.rocket_attack_path = gp.load_image("../resources/assets/Battle/Rocket/Rocket_110.png", rotation=-90, size=(3,9))
        self.basic_attack_sound = gp.pygame.mixer.Sound(gp.os.path.join(gp.os.path.dirname(gp.os.path.abspath(__file__)),"../resources/assets/Sound/Suara tembakan.mp3"))
        self.basic_attack_sound.set_volume(0.1)

        # Player skills
        self.skills = {
            "1": {"masif_att": {"active": False, "cooldown": 9000, "duration": 5000, "last_used": 0, "used": 0}},
            "2": {"double_att": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "3": {"rocket": {"active": False, "cooldown": 30000, "duration": 5000, "last_used": 0, "used": 0}},
            "4": {"shield": {"active": False, "cooldown": 20000, "duration": 10000, "last_used": 0, "used": 0}},
            "SPACE": {"regen": {"active": False, "cooldown": 30000, "duration": 2000, "last_used": 0, "used": 0}}
        }
    
    #  Memperbarui status player.
    def update(self):
        """Memperbarui status player."""
        
        # Mendapatkan waktu saat ini
        self.current_time = gp.pygame.time.get_ticks()
        
        # Menangani input pengguna, menggunakan skill, dan menggambar elemen UI
        self.handle_events()
        self.skill_use()
        self.draw_health_bar()
        self.draw_score()
        self.draw_icon_skill()
        
        # Mengatur fungsi basic attack dan menampilkan player di layar
        self.set_basicAttack_func()
        self.screen.blit(self.image, self.rect)
    
    # Menangani input pengguna untuk menggerakkan player dan menggunakan skill.
    def handle_events(self, option=False):
        """Menangani input pengguna untuk menggerakkan player dan menggunakan skill."""
        
        if self.handle_option:
            # Memeriksa tombol panah untuk menggerakkan player
            keys = gp.pygame.key.get_pressed()
            if keys[gp.pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[gp.pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[gp.pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[gp.pygame.K_DOWN]:
                self.rect.y += self.speed

            # Memeriksa tombol skill dan mengaktifkannya jika cooldown sudah berakhir
            for skill_key, skill_data in self.skills.items():
                for skill_name, skill_info in skill_data.items():
                    if keys[gp.pygame.key.key_code(skill_key)]:
                        if self.current_time - skill_info["last_used"] >= skill_info["cooldown"] or skill_info["last_used"] == 0:
                            if not skill_info["active"]:
                                skill_info["last_used"] = self.current_time
                                skill_info["active"] = True
                                skill_info["used"] += 1

            # Memastikan player tetap berada dalam batas layar permainan
            # gp.ic(self.player_win)
            if self.player_win is False:
                self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
                self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    # Menggunakan dan memproses efek skill player.
    def skill_use(self):
        """Menggunakan dan memproses efek skill player."""
        
        # Iterasi melalui semua skill player
        for skill_key, skill_data in self.skills.items():
            for skill_name, skill_info in skill_data.items():
                
                # Memproses skill "masif_att"
                if skill_name == "masif_att":
                    self.damage = 30 if skill_info["active"] else 25
                
                # Memproses skill "regen" untuk pemulihan kesehatan
                if skill_name == "regen" and not self.health > self.max_health:
                    if skill_info["active"]:
                        self.health += self.max_health * self.regen_hp
                
                # Memproses skill "shield" untuk melukis perisai biru
                if skill_name == "shield":
                    if self.shield <= 0:
                        skill_info["active"] = False
                    elif skill_info["active"]:
                        gp.pygame.draw.circle(self.screen, "blue", (self.rect.x + 35, self.rect.y + 25), 70)
                
                # Memproses skill "rocket" (belum diimplementasikan)
                if skill_name == "rocket":
                    pass
                
                # Memproses skill "double_att" untuk pengaturan basic attack
                if skill_name == "double_att":
                    self.type_basicAttack = "type_2" if skill_info["active"] else "type_1"
                    self.delay_basicAttack = 120 if skill_info["active"] else 180
                    self.damage += 10 if skill_info["active"] else 25
                    self.player_basic_attacks = self.player_basic_attacks_type2 if skill_info["active"] else self.player_basic_attacks_type1
                    self.available_basic_attacks = self.player_basic_attacks_type1 if skill_info["active"] else self.player_basic_attacks_type2
                    
                # Mematikan skill jika waktu yang cukup telah berlalu
                if self.current_time - skill_info["last_used"] >= skill_info["duration"]:
                    skill_info["active"] = False

    # Mengurangi kesehatan atau pelindung player berdasarkan jumlah kerusakan.
    def take_damage(self, damage=10):
        """Mengurangi kesehatan atau pelindung player berdasarkan jumlah kerusakan."""
        
        # Memeriksa apakah player memiliki pelindung (shield) aktif
        if self.skills["4"]["shield"]["active"] and self.shield > 0:
            # Mengurangi pelindung (shield) player
            self.shield -= damage
            self.shield = max(self.shield, 0)
        else:
            # Mengurangi kesehatan player jika tidak ada pelindung atau pelindung sudah habis
            self.health -= damage
            self.health = max(self.health, 0)

    # Menampilkan indikator kesehatan dan pelindung player di layar.
    def draw_health_bar(self):
        """Menampilkan indikator kesehatan dan pelindung player di layar."""
        
        # Menentukan warna dan nilai yang akan ditampilkan berdasarkan kondisi pelindung player
        color = ["green", "cyan"] if self.skills["4"]["shield"]["active"] and self.shield >= 0 else ["red", "green"]
        show = [self.shield, self.max_shield] if self.skills["4"]["shield"]["active"] and self.shield >= 0 else [self.health, self.max_health]
        
        # Menggambar indikator kesehatan dan pelindung
        gp.pygame.draw.rect(self.screen, color[0], (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (show[0] / show[1]) * self.rect.width
        gp.pygame.draw.rect(self.screen, color[1], (self.rect.x, self.rect.y - 10, current_health_width, 5))

    # Menampilkan skor player di layar.
    def draw_score(self):
        """Menampilkan skor player di layar."""
        
        # Membuat teks skor dengan font putih
        text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        
        # Menampilkan teks skor di koordinat (10, 10)
        self.screen.blit(text, (10, 10))
        
    # Membuat basic attack player.
    def create_basic_attack_player(self, AttackActor, player, last_time):
        """Membuat basic attack player."""
        
        # Memeriksa apakah sudah waktunya untuk membuat basic attack baru  
        if self.current_time - last_time >= self.delay_basicAttack:
            self.basic_attack_sound.play()
            # Membuat basic attack baru untuk setiap elemen dalam player_basic_attacks
            for double in self.player_basic_attacks:
                double.add(
                    AttackActor(
                        screen=self.screen,
                        actor=player, 
                        speed=self.basic_attack_speed, 
                        image=self.basic_attack_path,
                        attack_type="Spesial"
                    )
                )
            
            # Memperbarui waktu terakhir basic attack
            self.last_BasicAttack_time = self.current_time
        
    # Membuat serangan roket player.
    def create_rocket_attack_player(self, AttackActor, player, enemy_posisition):
        """Membuat rocket attack player."""
        
        self.player_rocket_attacks.add(
            AttackActor(
                    screen=self.screen,
                    actor=player,
                    speed=self.basic_attack_speed, 
                    image=self.rocket_attack_path,
                    target_position=enemy_posisition,
                    attack_type="rocket"
                )
            )
            
        # Memperbarui waktu terakhir  attack
        self.last_RocketAttack_time = self.current_time

    # Menampilkan ikon dan cooldown skill di layar.
    def draw_icon_skill(self):
        """Menampilkan ikon dan cooldown skill di layar."""
        
        # Iterasi melalui semua skill dan menampilkan ikon serta cooldown
        for i, (skill_key, skill_data) in enumerate(self.skills.items(), start=1):
            for skill_name, skill_info in skill_data.items():
                
                # Menghitung cooldown dan memastikan nilainya tidak kurang dari 0
                calculate_cooldown = lambda skill_info, current_time: max(0, ((skill_info["last_used"] - self.current_time) + skill_info["cooldown"]) // 1000) if skill_info["used"] != 0 else 0
                cooldown = calculate_cooldown(skill_info, self.current_time)

                # Menggambar area untuk menampilkan ikon dan cooldown
                gp.pygame.draw.rect(self.screen, "white", [10, 70 + i * 60, 150, 50])
                
                # Menampilkan teks dengan informasi skill dan cooldown
                text = self.font.render(f"{skill_name}: {cooldown}", True, "black")
                self.screen.blit(text, (10, 80 + i * 60))

    # Menetapkan fungsi untuk menampilkan basic attack player di layar.
    def set_basicAttack_func(self):
        """Menetapkan fungsi untuk menampilkan basic attack player di layar."""
        
        # Fungsi lokal untuk memindahkan basic attack
        def bullet_move(attacks, offset_x=0):
            for attack in attacks:
                attack.rect.y -= attack.speed
                self.screen.blit(attack.image, (attack.rect.x + offset_x, attack.rect.y))

        # Menampilkan basic attack player yang sedang aktif
        if len(self.player_basic_attacks) > 0:
            for attacks in range(len(self.player_basic_attacks)):
                bullet_move(self.player_basic_attacks[attacks], offset_x=(20*attacks)-(10*len(self.player_basic_attacks)//(attacks+1)))

        # Menampilkan basic attack player yang masih tersedia
        if len(self.available_basic_attacks) > 0:
            for attacks in range(len(self.available_basic_attacks)):
                bullet_move(self.available_basic_attacks[attacks], offset_x=(20*attacks)-(10*len(self.available_basic_attacks)//(attacks+1)))
