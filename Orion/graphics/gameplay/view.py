from .. import gameplay as gp
import sys
import os
from icecream import ic
from .battle import Level1, Level2, Level3, Level4, Level5

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

# object button dalam tampilan 
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

# class untuk mengatur tampilan beranda, select lvl, page win dan lose player
class Views:
    """
    Kelas untuk mengelola tampilan dalam permainan.

    Args:
    - screen: Objek layar permainan.
    - screen_width (int): Lebar layar permainan.
    - screen_height (int): Tinggi layar permainan.
    - window_size: Ukuran jendela permainan.

    Attributes:
    - screen: Objek layar permainan.
    - screen_width (int): Lebar layar permainan.
    - screen_height (int): Tinggi layar permainan.
    - window_size: Ukuran jendela permainan.
    - path: Path menuju direktori tampilan.
    - battle: Objek tampilan pertempuran.
    - background_battle: Gambar latar belakang tampilan pertempuran.
    - buttons: Grup sprite tombol.
    - background_home: Gambar latar belakang tampilan rumah.
    - background_select_lvl: Gambar latar belakang tampilan pemilihan level.
    - set_background: Gambar latar belakang yang diatur saat ini.
    - background_page_player_lose: Gambar latar belakang tampilan pemain kalah.
    - background_page_player_win: Gambar latar belakang tampilan pemain menang.
    - start_time: Waktu mulai tampilan.
    - start_time_index: Indeks waktu mulai.
    - Level_now: Level saat ini.

    Methods:
    - __init__: Inisialisasi objek tampilan.
    """
    
    def __init__(self, screen, screen_width, screen_height, window_size):
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
        self.background_page_player_lose = self.func_set_background("../resources/assets/GAME OVER/LOSE POLOSAN.png", self.window_size)
        self.background_page_player_win = self.func_set_background("../resources/assets/GAME OVER/WIN POLOSAN.png", self.window_size)

        self.start_time = gp.pygame.time.get_ticks()
        self.start_time_index = 0
        self.Level_now = None
        
        self.save_game = gp.load_from_json("../resources/save_data.json")
        
        self.button_lock = load_image("../resources/assets/level select/level lock button.png")
        self.button_level_save = {
            "lvl 1" : {"button" : load_image("../resources/assets/level select/button lvl 1.png"), "action":[self.set_path, self.set_Level], "parameters":[["Battle"], [Level1, [self.screen, self.screen_width, self.screen_height]]]},
            "lvl 2" : {"button" : load_image("../resources/assets/level select/button lvl 2.png"), "action":[self.set_path, self.set_Level], "parameters":[["Battle"], [Level2, [self.screen, self.screen_width, self.screen_height]]]},
            "lvl 3" : {"button" : load_image("../resources/assets/level select/button lvl 3.png"), "action":[self.set_path, self.set_Level], "parameters":[["Battle"], [Level3, [self.screen, self.screen_width, self.screen_height]]]},
            "lvl 4" : {"button" : load_image("../resources/assets/level select/button lvl 4.png"), "action":[self.set_path, self.set_Level], "parameters":[["Battle"], [Level4, [self.screen, self.screen_width, self.screen_height]]]},
            "lvl 5" : {"button" : load_image("../resources/assets/level select/button lvl 5.png"), "action":[self.set_path, self.set_Level], "parameters":[["Battle"], [Level5, [self.screen, self.screen_width, self.screen_height]]]}
        }
        
        self.button_level_set = {
            "lvl 1" : self.button_level_save["lvl 1"],
            "lvl 2" : {"button":self.button_lock, "action":None, "parameters":None},
            "lvl 3" : {"button":self.button_lock, "action":None, "parameters":None},
            "lvl 4" : {"button":self.button_lock, "action":None, "parameters":None},
            "lvl 5" : {"button":self.button_lock, "action":None, "parameters":None}
        }
        self.current_lvl = "lvl 1"
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.sound_files = {
            "button click": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/button click.mp3")),
            "home backsound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/home backsound.mp3")),
            "win sound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/win sound.mp3")),
            "lose sound": gp.pygame.mixer.Sound(os.path.join(current_directory,"../resources/assets/Sound/lose sound.mp3")),
        }
        
        for sound in self.sound_files.values():
            sound.set_volume(0.3)
        
        self.sound_files["home backsound"].play(maxtime=-1)

    # Menambahkan tombol ke grup tombol
    def add_button(self, image, pos_x, pos_y, action=None, parameters=[]):
        """
        Parameters:
        - image: Gambar tombol.
        - pos_x (int): Koordinat x posisi tombol.
        - pos_y (int): Koordinat y posisi tombol.
        - action (list): Daftar fungsi aksi yang akan dijalankan saat tombol diklik.
        - parameters (list): Daftar parameter yang akan diteruskan ke fungsi aksi (opsional).
        """
        button = Button(image, pos_x, pos_y, action, parameters)
        self.buttons.add(button)

    # Menampilkan tampilan menu level.
    def views_menu_lvl(self):
        data_buttons = {
            'btn_1':{
                'image': self.button_level_set["lvl 1"]["button"],
                'pos_x': self.screen_width // 4.2,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': self.button_level_set["lvl 1"]["action"],
                'parameters': self.button_level_set["lvl 1"]["parameters"]
            },
            'btn_2':{
                'image': self.button_level_set["lvl 4"]["button"],
                'pos_x': self.screen_width // 2.9,
                'pos_y': self.screen_height // 1.7 - 70,
                'action': self.button_level_set["lvl 4"]["action"],
                'parameters': self.button_level_set["lvl 4"]["parameters"]
            },
            'btn_3':{
                'image': self.button_level_set["lvl 2"]["button"],
                'pos_x': self.screen_width // 2.2,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': self.button_level_set["lvl 2"]["action"],
                'parameters': self.button_level_set["lvl 2"]["parameters"]
            },
            'btn_4':{
                'image': self.button_level_set["lvl 3"]["button"],
                'pos_x': self.screen_width // 1.5,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': self.button_level_set["lvl 3"]["action"],
                'parameters': self.button_level_set["lvl 3"]["parameters"]
            },
            'btn_5':{
                'image': self.button_level_set["lvl 5"]["button"],
                'pos_x': self.screen_width // 1.8,
                'pos_y': self.screen_height // 1.7 - 70,
                'action': self.button_level_set["lvl 5"]["action"],
                'parameters': self.button_level_set["lvl 5"]["parameters"]
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
    
    # Menampilkan tampilan Beranda.
    def Beranda(self):
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
    
    # Menampilkan tampilan page player win
    def page_player_win(self):
        data_buttons = {
            'btn_home':{
                'image':load_image("../resources/assets/GAME OVER/HOME.png"),
                'pos_x': self.screen_width // 4.2 - 50,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path],
                'parameters': [["Views"]]
            },
            'btn_retry':{
                'image': load_image("../resources/assets/GAME OVER/RETRYBTN.png"),
                'pos_x': self.screen_width // 2 + 270,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [self.Level_now, [self.screen, self.screen_width, self.screen_height]]]
            },
            'btn_next':{
                'image': load_image("../resources/assets/GAME OVER/NEXT BTN.png"),
                'pos_x': self.screen_width // 2.4 + 15,
                'pos_y': self.screen_height // 1.7 - 180,
                'action': [self.next_level ,self.set_path, self.set_Level],
                'parameters': [[None],["Battle"], [self.Level_now, [self.screen, self.screen_width, self.screen_height]]]
            }
        }
        for button in data_buttons.values():
            self.add_button(
                button['image'],
                button['pos_x'], button['pos_y'],
                action=button['action'],
                parameters=button['parameters'])
        
    # Menampilkan tampilan page player lose
    def page_player_lose(self):
        """
            Menampilkan tampilan Views.
        """
        data_buttons = {
            'btn_home':{
                'image':load_image("../resources/assets/GAME OVER/HOME.png"),
                'pos_x': self.screen_width // 4.2 - 20,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path],
                'parameters': [["Views"]]
            },
            'btn_retry':{
                'image': load_image("../resources/assets/GAME OVER/RETRYBTN.png"),
                'pos_x': self.screen_width // 2.2 + 250,
                'pos_y': self.screen_height // 1.9 - 160,
                'action': [self.set_path, self.set_Level],
                'parameters': [["Battle"], [self.Level_now, [self.screen, self.screen_width, self.screen_height]]]
            }
        }
        for button in data_buttons.values():
            self.add_button(
                button['image'], 
                button['pos_x'], button['pos_y'], 
                action=button['action'], 
                parameters=button['parameters']) 
    
    # Merender tampilan berdasarkan ukuran layar yang diberikan.
    def rendering(self, height, width):
        """
        Parameters:
        - height (int): Tinggi layar.
        - width (int): Lebar layar.

        Returns:
        - bool: True jika tampilan masih berjalan, False jika pengguna menutup jendela.
        """
        # Menetapkan ukuran layar yang baru
        self.screen_height = height
        self.screen_width = width
        
        # print(self.save_data)
        
        # Mengosongkan grup tombol
        self.buttons.empty()

        # Menggambar latar belakang
        self.screen.blit(self.set_background, (0, 0))
        
        # Menentukan tindakan berdasarkan path
        if self.path == "Views":
            self.Beranda()
            self.set_background = self.background_home
        elif self.path == "Views/Stage":
            # set type button
            self.load_level_button()
            
            self.views_menu_lvl()
            self.set_background = self.background_select_lvl
        elif self.path == "Battle":
            condition = self.battle.run(self.start_time_index == 0)
            try:
                if condition is not None:
                    self.start_time_index+=1
                    if condition is True:
                        self.set_background = self.background_page_player_win
                        self.path = "Player Win"
                        self.start_time_index = 0
                    elif condition is False:
                        self.set_background = self.background_page_player_lose
                        self.path = "Player Lose"
                        self.start_time_index = 0
                else:
                    self.set_background = self.background_battle
            except Exception as e:
                print('error',e)
                
        elif self.path == "Player Win":
            self.page_player_win()
        elif self.path == "Player Lose":
            self.page_player_lose()
            

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

    # Menetapkan gambar latar belakang.
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
        
    # Mengatur path berdasarkan input click user.
    def set_path(self, path, next_sound=True):
        """

        Parameters:
        - path (str): Path baru.
        """
        if next_sound is True:
            for sound in self.sound_files.values():
                sound.stop()
            
            if path == "Views":
                self.sound_files["home backsound"].play(maxtime=-1)
        self.path = path
        
    # Mengatur level berdasarkan input click dari user
    def set_Level(self, Level, parameters):
        """
        Mengatur level berdasarkan input click dari user

        Parameters:
        - Level: Kelas level.
        - parameters (list): Daftar parameter level.
        """
        if Level == Level1:
            self.current_lvl = "lvl 1"
        elif Level == Level2:
            self.current_lvl = "lvl 2"
        elif Level == Level3:
            self.current_lvl = "lvl 3"
        elif Level == Level4:
            self.current_lvl = "lvl 4"
        elif Level == Level5:
            self.current_lvl = "lvl 5"
        
        self.Level_now = Level
        self.battle = self.Level_now(*parameters)
        # merubah background battle sesuai dengan level
        self.background_battle = self.func_set_background(self.battle.path_image_background, self.window_size)
    
    # Pindah ke level selanjutnya.
    def next_level(self):
        """
        Pindah ke level selanjutnya.

        Notes:
        - Fungsi ini hanya mengubah level saat ini ke level selanjutnya.
        """
        if self.Level_now == Level1:
            self.Level_now = Level2
        elif self.Level_now == Level2:
            self.Level_now = Level3
        elif self.Level_now == Level3:
            self.Level_now = Level4
        elif self.Level_now == Level4:
            self.Level_now = Level5
        else:
            self.path = "Beranda"
            
        for sound in self.sound_files.values():
            sound.stop()

    # set button type
    def load_level_button(self):
        self.save_data = gp.load_from_json("../resources/save_data.json")
        button_level_save = self.button_level_save
        button_level_set = self.button_level_set
        
        for data in self.save_data:
            if int(self.save_data[data][0]) >= 1000 or self.save_data[data][1] == "True":
                button_level_set[data] = button_level_save[data]
            else:
                button_level_set[data] = {"button": self.button_lock, "action": None, "parameters": None}
