from .. import gameplay as gp

class Friends:
    def __init__(self, screen_width, screen_height, screen):
       
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load friend image and get its rect
        self.image = gp.load_image("../resources/assets/Battle/friend.png",size=(100,100), colorkey=("grey"))
        self.image_rocket = gp.load_image("../resources/assets/Battle/Rocket/Rocket_061.png", scale=50)
        self.rect = self.image.get_rect()
        self.font = gp.pygame.font.Font(None, 36)

        # Set initial position
        self.rect.centerx = screen_width // 2 + 90  # Menambah 50 pixel ke posisi awal x
        self.rect.bottom = screen_height + 100

        # Friends attributes
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
        self.friend_rocket_attacks = gp.pygame.sprite.Group()
        self.friend_basic_attacks = [gp.pygame.sprite.Group() for i in range(1)]
        self.available_basic_attacks = []
        self.friend_win = False
        self.handle_option = True
        self.basic_attack_path = gp.load_image("../resources/assets/Battle/Laser Sprites/11.png", scale=3)
        self.rocket_attack_path = gp.load_image("../resources/assets/Battle/Rocket/Rocket_110.png", rotation=-90, size=(3,9))
        self.basic_attack_sound = gp.pygame.mixer.Sound(gp.os.path.join(gp.os.path.dirname(gp.os.path.abspath(__file__)),"../resources/assets/Sound/Suara tembakan.mp3"))
        self.basic_attack_sound.set_volume(0.1)

    #  Memperbarui status friend.
    def update(self):
        """Memperbarui status friend."""
        
        # Mendapatkan waktu saat ini
        self.current_time = gp.pygame.time.get_ticks()
        
        # Menangani input pengguna, menggunakan skill, dan menggambar elemen UI
        self.handle_events()
        self.draw_health_bar()
        self.draw_score()
        
        # Mengatur fungsi basic attack dan menampilkan friend di layar
        self.set_basicAttack_func()
        self.screen.blit(self.image, self.rect)
    
    # Menangani input pengguna untuk menggerakkan friend dan menggunakan skill.
    def handle_events(self, option=False):
        """Menangani input pengguna untuk menggerakkan friend dan menggunakan skill."""
        
        if self.handle_option:
            # Memeriksa tombol panah untuk menggerakkan friend
            keys = gp.pygame.key.get_pressed()
            if keys[gp.pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[gp.pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[gp.pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[gp.pygame.K_DOWN]:
                self.rect.y += self.speed

            

            # Memastikan friend tetap berada dalam batas layar permainan
            # gp.ic(self.friend_win)
            if self.friend_win is False:
                self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
                self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))
   
    # Menampilkan indikator kesehatan dan pelindung friend di layar
    def draw_health_bar(self):
        """Menampilkan indikator kesehatan dan pelindung friend di layar."""
        

        # Menggambar indikator kesehatan dan pelindung
        gp.pygame.draw.rect(self.screen, "cyan", (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        current_health_width = (self.health / self.max_health) * self.rect.width
        gp.pygame.draw.rect(self.screen, "green", (self.rect.x, self.rect.y - 10, current_health_width, 5))

    # Menampilkan skor friend di layar.
    def draw_score(self):
        """Menampilkan skor friend di layar."""
        
        # Membuat teks skor dengan font putih
        text = self.font.render(f"Skor: {self.score}", True, (255, 255, 255))
        
        # Menampilkan teks skor di koordinat (10, 10)
        self.screen.blit(text, (10, 10))
        
    # Membuat basic attack friend.
    def create_basic_attack_friend(self, AttackActor, friend, last_time):
        """Membuat basic attack friend."""
        
        # Memeriksa apakah sudah waktunya untuk membuat basic attack baru  
        if self.current_time - last_time >= self.delay_basicAttack:
            self.basic_attack_sound.play()
            # Membuat basic attack baru untuk setiap elemen dalam friend_basic_attacks
            for double in self.friend_basic_attacks:
                double.add(
                    AttackActor(
                        screen=self.screen,
                        actor=friend, 
                        speed=self.basic_attack_speed, 
                        image=self.basic_attack_path,
                        attack_type="Spesial"
                    )
                )
            
            # Memperbarui waktu terakhir basic attack
            self.last_BasicAttack_time = self.current_time

    # Menetapkan fungsi untuk menampilkan basic attack friend di layar.
    def set_basicAttack_func(self):
        """Menetapkan fungsi untuk menampilkan basic attack friend di layar."""
        
        # Fungsi lokal untuk memindahkan basic attack
        def bullet_move(attacks, offset_x=0):
            for attack in attacks:
                attack.rect.y -= attack.speed
                self.screen.blit(attack.image, (attack.rect.x + offset_x, attack.rect.y))

        # Menampilkan basic attack friend yang sedang aktif
        if len(self.friend_basic_attacks) > 0:
            for attacks in range(len(self.friend_basic_attacks)):
                bullet_move(self.friend_basic_attacks[attacks], offset_x=(20*attacks)-(10*len(self.friend_basic_attacks)//(attacks+1)))