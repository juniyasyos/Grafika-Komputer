import pygame
import sys
from .battle import Battle
import os

def load_image(image_filename):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        image = pygame.image.load(image_path).convert_alpha()
        width =int(image.get_width() * 0.9)
        height = int(image.get_height() * 0.9)
        return pygame.transform.scale(image,(width,height))
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e


class Beranda:
    def __init__(self, screen, screen_width, screen_height, background):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.set_background = background
        self.width_lvl = 0
        self.height_lvl = 0
        self.path = "Beranda"
        self.battle = Battle(self.screen, self.screen_width, self.screen_height)
        self.buttons = []

    def add_button(self, color, size, color_hover, text, pos_x, pos_y, text_color='black', text_color_hover="white", action=None, parameters=[]):
        button_data = {
            "color": color,
            "size": size,
            "color_hover": color_hover,
            "text": text,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "text_color": text_color,
            "text_color_hover": text_color_hover,
            "action": action,
            "parameters": parameters
        }
        self.buttons.append(button_data)
    
    def add_image_button(self, image, pos_x, pos_y, action=None, parameters=[]):
        button_data = {
            "image": image,  # Gambar tombol
            "image_hover": image,  
            "pos_x": pos_x,  # Koordinat X
            "pos_y": pos_y,  # Koordinat Y
            "action": action,  # Aksi yang akan dijalankan saat tombol ditekan
            "parameters": parameters  # Parameter yang diperlukan untuk aksi
        }
        self.buttons.append(button_data)


    def handle_button_click(self, button):
        if button["action"] is not None:
            for i in range(len(button["action"])):
                if button["parameters"] == []:
                    button["action"][i]()
                else:
                    if button["parameters"][i][0] is None:
                        button["action"][i]()
                    else:
                        if pygame.mouse.get_pressed()[0] == 1:
                            button["action"][i](*button["parameters"][i])

    def draw_button(self, button):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if isinstance(button.get("image"), pygame.Surface):
            # Jika tombol adalah tombol gambar
            button_rect = button["image"].get_rect(topleft=(button["pos_x"], button["pos_y"]))
            if button_rect.collidepoint(mouse_pos):
                self.screen.blit(button["image_hover"], (button["pos_x"], button["pos_y"]))
                if mouse_click[0] == 1:
                    self.handle_button_click(button)
            else:
                self.screen.blit(button["image"], (button["pos_x"], button["pos_y"]))
        else:
            # Jika tombol adalah tombol teks
            if button["pos_x"] < mouse_pos[0] < button["pos_x"] + button["size"][0] and button["pos_y"] < mouse_pos[1] < button["pos_y"] + button["size"][1]:
                pygame.draw.rect(self.screen, button["color_hover"], (button["pos_x"], button["pos_y"], button["size"][0], button["size"][1]), border_radius=10)
                if mouse_click[0] == 1:
                    self.handle_button_click(button)
            else:
                pygame.draw.rect(self.screen, button["color"], (button["pos_x"], button["pos_y"], button["size"][0], button["size"][1]), border_radius=10)

            font = pygame.font.Font(None, 24)
            text_hover = font.render(button["text"], True, button["text_color_hover"] if button["pos_x"] < mouse_pos[0] < button["pos_x"] + button["size"][0] and button["pos_y"] < mouse_pos[1] < button["pos_y"] + button["size"][1] else button["text_color"])
            text_rect = text_hover.get_rect(center=(button["pos_x"] + button["size"][0] / 2, button["pos_y"] + button["size"][1] / 2))
            self.screen.blit(text_hover, text_rect)


    def views_menu_lvl(self):
        pygame.draw.rect(self.screen, 'silver', (self.width_lvl // 6 + 400, self.height_lvl // 6, self.width_lvl // 1.5 - 400, self.height_lvl // 1.5 + 100), border_radius=10)
        self.add_button('cyan', (400, 80), 'black', "Stage 1", self.width_lvl // 2, self.height_lvl // 2 - 160, action=[self.set_path], parameters=[["Battle"]])
        self.add_button('cyan', (400, 80), 'black', "Stage 2", self.width_lvl // 2, self.height_lvl // 2 - 70, action=[self.set_path], parameters=[["Battle"]])
        self.add_button('cyan', (400, 80), 'black', "Stage 3", self.width_lvl // 2, self.height_lvl // 2 + 20, action=[self.set_path], parameters=[["Battle"]])
        self.add_button('cyan', (400, 80), 'black', "Back", self.width_lvl // 2, self.height_lvl // 2 + 260, action=[self.set_path], parameters=[["Beranda"]])

    def views_Beranda(self, width, height):
        self.add_image_button(image=(load_image("../resources/assets/Menu/start_button.png")), pos_x=width // 3 + 84, pos_y=height // 2 - 150, action=[self.set_path], parameters=[["Battle"]])
        self.add_image_button(image=(load_image("../resources/assets/Menu/inventory_button.png")), pos_x=width // 3 + 84, pos_y=height // 2 + 20)
        self.add_image_button(image=(load_image("../resources/assets/Menu/exit_button.png")), pos_x=width // 3 + 84, pos_y=height // 2 +200, action=[pygame.quit, sys.exit])

    def rendering(self, color, height, width):
        self.height_lvl = height
        self.width_lvl = width
        self.buttons = []

        if self.path == "Beranda":
            self.views_Beranda(width=width, height=height)
        elif self.path == "Beranda/Stage":
            self.views_menu_lvl()
        elif self.path == "Battle":
            self.screen.fill((0,0,0))
            self.battle.run()
        else:
            self.views_Beranda(width=width, height=height)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Tangani event resize jendela
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH = event.w  # Perbarui lebar layar
                self.HEIGHT = event.h  # Perbarui tinggi layar
                self.WINDOW_SIZE = (self.WIDTH, self.HEIGHT)
                self.set_background = load_image("../resources/assets/Menu/home.png")

        for button in self.buttons:
            self.draw_button(button)
        return True
        
    def set_path(self, path):
        self.path = path
