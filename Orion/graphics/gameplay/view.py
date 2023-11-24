from .. import gameplay as gp
import sys
import os
from .battle import Level1, Level2

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
        self.add_button(load_image("../resources/assets/level select/button lvl 1.png"), self.screen_width // 4.2, self.screen_height // 1.9 - 160, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/level select/level lock button.png"), self.screen_width // 4.2, self.screen_height // 1.7 - 70, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level2, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/level select/button lvl 2.png"), self.screen_width // 2.2, self.screen_height // 1.9 - 160, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level2, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/level select/level lock button.png"), self.screen_width // 2.2, self.screen_height // 1.7 - 70, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/level select/button lvl 3.png"), self.screen_width // 1.5, self.screen_height // 1.9 - 160, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/level select/level lock button.png"), self.screen_width // 1.5, self.screen_height // 1.7 - 70, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        
    def Beranda(self):
        """
        Menampilkan tampilan Views.
        """
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 - 150, action=[self.set_path, self.set_Level], parameters=[["Views/Stage"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/Menu/inventory_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 + 20)
        self.add_button(load_image("../resources/assets/Menu/exit_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 + 200, action=[gp.pygame.quit, sys.exit])

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
        elif self.path == "Views/Stage":
            self.views_menu_lvl()
            self.set_background = self.background_select_lvl
        elif self.path == "Battle":
            self.battle.run()
            self.set_background = self.background_battle
        else:
            self.Beranda()

        # Memperbarui grup tombol
        self.buttons.update()

        # Menangani interaksi dengan tombol
        for button in self.buttons:
            if button.rect.collidepoint(gp.pygame.mouse.get_pos()):
                gp.pygame.draw.rect(self.screen, 'cyan', button.rect, border_radius=10)
                if gp.pygame.mouse.get_pressed()[0] == 1:
                    button.handle_click()
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
        

    def set_path(self, path):
        """
        Mengatur path berdasarkan input.

        Parameters:
        - path (str): Path baru.
        """
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
