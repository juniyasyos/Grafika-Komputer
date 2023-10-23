import pygame
import sys
from .battle import Battle

class Beranda:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
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

    def views_Beranda(self, color, width, height):
        pygame.draw.rect(self.screen, color, (width // 6, height // 6, width // 1.5, height // 1.5), border_radius=10)
        self.add_button('white', (400, 80), 'black', "Battle", width // 2 + 30, height // 2 - 100, action=[self.set_path, self.views_menu_lvl], parameters=[["Beranda/Stage"], [None]])
        self.add_button('white', (400, 80), 'black', "Inventory", width // 2 + 30, height // 2 + 20)
        self.add_button('white', (400, 80), 'black', "Quit", width // 2 + 30, height // 2 + 140, action=[pygame.quit, sys.exit])

    def rendering(self, color, height, width):
        self.height_lvl = height
        self.width_lvl = width
        self.buttons = []

        if self.path == "Beranda":
            self.views_Beranda(color=color, width=width, height=height)
        elif self.path == "Beranda/Stage":
            self.views_menu_lvl()
        elif self.path == "Battle":
            self.battle.run()
        else:
            self.views_Beranda(color=color, width=width, height=height)
        
        for button in self.buttons:
            self.draw_button(button)

    def set_path(self, path):
        self.path = path
