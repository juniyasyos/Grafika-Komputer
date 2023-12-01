from .. import gameplay as gp
import sys
import os
from .battle import Level1, Level2, Level3

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        image = gp.pygame.image.load(image_path).convert_alpha()
        width =int(image.get_width() * 0.9)
        height = int(image.get_height() * 0.9)
        return gp.pygame.transform.scale(image,(width,height))
    except gp.pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e

class Button(gp.pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, action, parameters=[]):
        """
        Inisialisasi objek tombol.

        Parameters:
        - image: Gambar tombol.
        - pos_x (int): Koordinat x posisi tombol.
        - pos_y (int): Koordinat y posisi tombol.
        - action (list): Daftar fungsi aksi yang akan dijalankan saat tombol diklik.
        - parameters (list): Daftar parameter yang akan diteruskan ke fungsi aksi (opsional).
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.action = action
        self.parameters = parameters

    def handle_click(self):
        """
        Menangani klik pada tombol dan menjalankan fungsi aksi yang terkait.
        """
        if self.action is not None:
            for i in range(len(self.action)):
                if not self.parameters or self.parameters[i][0] is None:
                    # Menjalankan fungsi aksi tanpa parameter jika tidak ada parameter atau parameter None
                    self.action[i]()
                else:
                    # Menjalankan fungsi aksi dengan parameter jika tombol kiri mouse ditekan
                    if gp.pygame.mouse.get_pressed()[0] == 1:
                        self.action[i](*self.parameters[i])


class Views:
    def __init__(self, screen, screen_width, screen_height, window_size):
        """
        Inisialisasi tampilan Views.

        Parameters:
        - screen: Objek layar Pygame.
        - screen_width (int): Lebar layar.
        - screen_height (int): Tinggi layar.
        - window_size (tuple): Ukuran jendela tampilan.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_size = window_size
        self.path = "Views"
        self.battle = None
        self.background_battle = None
        self.buttons = gp.pygame.sprite.Group()
        self.background_home = self.func_set_background("../resources/assets/Menu/home.png", self.window_size)
        self.background_select_lvl = self.func_set_background("../resources/assets/level select/level select.png", self.window_size)
        self.set_background = self.background_home
        
        self.start_time = gp.pygame.time.get_ticks()
        self.start_time_index = 0
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.sound_files = {
            "button click": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/button click.mp3")),
            "home backsound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/home backsound.mp3")),
            "win sound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/win sound.mp3")),
            "battle sound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/battle sound .mp3")),
        }
        
        for sound in self.sound_files.values():
            sound.set_volume(0.3)
        
        self.sound_files["home backsound"].play(maxtime=-1)

    def add_button(self, image, pos_x, pos_y, action=None, parameters=[]):
        """
        Menambahkan tombol ke grup tombol.

        Parameters:
        - image: Gambar tombol.
        - pos_x (int): Koordinat x posisi tombol.
        - pos_y (int): Koordinat y posisi tombol.
        - action (list): Daftar fungsi aksi yang akan dijalankan saat tombol diklik.
        - parameters (list): Daftar parameter yang akan diteruskan ke fungsi aksi (opsional).
        """
        button = Button(image, pos_x, pos_y, action, parameters)
        self.buttons.add(button)

    def views_menu_lvl(self):
        """
        Menampilkan tampilan menu level.
        """
        data_buttons = {
            'btn_1':{
                'image': load_image("../resources/assets/level select/button lvl 1.png"),
                'pos_x': self.screen_width // 4.2,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [Level1, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_2':{
                'image': load_image("../resources/assets/level select/level lock button.png"),
                'pos_x': self.screen_width // 2.9,
                'pos_y': self.screen_height // 1.7 - 70,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [Level1, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_3':{
                'image': load_image("../resources/assets/level select/button lvl 2.png"),
                'pos_x': self.screen_width // 2.2,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [Level2, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_4':{
                'image': load_image("../resources/assets/level select/button lvl 3.png"),
                'pos_x': self.screen_width // 1.5,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [Level3, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_5':{
                'image': load_image("../resources/assets/level select/level lock button.png"),
                'pos_x': self.screen_width // 1.8,
                'pos_y': self.screen_height // 1.7 - 70,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [Level2, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_play':{
                'image': load_image("../resources/assets/level select/button play.png"),
                'pos_x': self.screen_width // 1.5,
                'pos_y': self.screen_height // 1.2 - 70,
                'action': [self.set_path],
                'parameters': [["Views"]]
            },
            'btn_home':{
                'image': load_image("../resources/assets/level select/button home.png"),
                'pos_x': self.screen_width // 6 + 60,
                'pos_y': self.screen_height // 1.2 - 70,
                'action': [self.set_path],
                'parameters': [["Views",False]]
            }
        }
        for button in data_buttons.values():
            self.add_button(
                button['image'], 
                button['pos_x'], button['pos_y'], 
                action=button['action'], 
                parameters=button['parameters'])
        
    def Beranda(self):
        """
        Menampilkan tampilan Views.
        """
        data_buttons = {
            'btn_start':{
                'image':load_image("../resources/assets/Menu/start_button.png"),
                'pos_x': self.screen_width // 3 + 84,
                'pos_y': self.screen_height // 2 - 150,
                'action' : [self.set_path, self.set_Level],
                'parameters': [["Views/Stage",False], [Level1, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_inventory':{
                'image':load_image("../resources/assets/Menu/inventory_button.png"),
                'pos_x': self.screen_width // 3 + 84,
                'pos_y': self.screen_height // 2 + 20,
                'action' : [],
                'parameters': []
            },
            'btn_exit':{
                'image':load_image("../resources/assets/Menu/exit_button.png"),
                'pos_x': self.screen_width // 3 + 84,
                'pos_y': self.screen_height // 2 + 200,
                'action' : [gp.pygame.quit, sys.exit],
                'parameters': []
            }
        }
        
        for button in data_buttons.values():
            self.add_button(
                button['image'], 
                button['pos_x'], button['pos_y'], 
                action=button['action'], 
                parameters=button['parameters'])
    
    
    def page_player_win(self):
        pass
    
    def page_player_lose(self):
        pass
    
    def rendering(self, height, width):
        """
        Merender tampilan berdasarkan ukuran layar yang diberikan.

        Parameters:
        - height (int): Tinggi layar.
        - width (int): Lebar layar.

        Returns:
        - bool: True jika tampilan masih berjalan, False jika pengguna menutup jendela.
        """
        # Menetapkan ukuran layar yang baru
        self.screen_height = height
        self.screen_width = width
        
        # Mengosongkan grup tombol
        self.buttons.empty()

        # Menggambar latar belakang
        self.screen.blit(self.set_background, (0, 0))
        
        # Menentukan tindakan berdasarkan path
        if self.path == "Views":
            self.Beranda()
            self.set_background = self.background_home
        elif self.path == "Views/Stage":
            self.views_menu_lvl()
            self.set_background = self.background_select_lvl
        elif self.path == "Battle":
            condition = self.battle.run()
            if condition is True:
                print("player win")
                self.page_player_win()
                self.path = "Player Win"
            elif condition is False:
                self.page_player_lose()
                print("player lose")
                self.path = "Player Lose"
            else:
                self.set_background = self.background_battle

        # Memperbarui grup tombol
        self.buttons.update()

        # Menangani interaksi dengan tombol
        for button in self.buttons:
            if button.rect.collidepoint(gp.pygame.mouse.get_pos()):
                gp.pygame.draw.rect(self.screen, 'cyan', (button.rect.x-3, button.rect.y+5, button.rect.width, button.rect.height+5), border_radius=10)
                self.screen.blit(button.image,[(button.rect.x, button.rect.y+6), (button.rect.width, button.rect.height)])
                if gp.pygame.mouse.get_pressed()[0] == 1:
                    self.sound_files["button click"].play()
                    button.handle_click()
            else:
                self.screen.blit(button.image, button.rect.topleft)

        # Menangani event Pygame
        for event in gp.pygame.event.get():
            if event.type == gp.pygame.QUIT:
                return False
            elif event.type == gp.pygame.VIDEORESIZE:
                # Menangani perubahan ukuran layar
                self.screen_width = event.w
                self.screen_height = event.h
                self.set_background = self.background_home

        # Mengembalikan True agar permainan tetap berjalan
        return True


    def func_set_background(self, file, window_size):
        """
        Menetapkan gambar latar belakang.

        Parameters:
        - file (str): Nama file gambar latar belakang.
        - window_size (tuple): Ukuran jendela tampilan.

        Returns:
        - pygame.Surface: Gambar latar belakang yang sudah diubah ukurannya sesuai dengan window_size.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__)) 
        image_path = os.path.join(current_directory, file) 
    
        try:
            image = gp.pygame.image.load(image_path).convert()
            scaled_image = gp.pygame.transform.scale(image, window_size)
            return scaled_image
        except gp.pygame.error as e:
            print(f"Failed to load image: {image_filename}")
            raise e
        

    def set_path(self, path, next_sound=True):
        """
        Mengatur path berdasarkan input.

        Parameters:
        - path (str): Path baru.
        """
        
        if next_sound is True:
            for sound in self.sound_files.values():
                sound.stop()
            
            if path == "Views":
                self.sound_files["home backsound"].play(maxtime=-1)
            elif path == "Battle":
                self.sound_files["battle sound"].play(maxtime=-1)
        
        self.path = path
        
    def set_Level(self, Level, parameters):
        """
        Mengatur level berdasarkan input.

        Parameters:
        - Level: Kelas level.
        - parameters (list): Daftar parameter level.
        """
        self.battle = Level(*parameters)
        # merubah background battle sesuai dengan level
        self.background_battle = self.func_set_background(self.battle.path_image_background, self.window_size)

