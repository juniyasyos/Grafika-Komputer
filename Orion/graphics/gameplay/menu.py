from .. import gameplay as gp
import sys
import os
from .battle import Level1

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
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.action = action
        self.parameters = parameters

    def handle_click(self):
        if self.action is not None:
            for i in range(len(self.action)):
                if not self.parameters or self.parameters[i][0] is None:
                    self.action[i]()
                else:
                    if gp.pygame.mouse.get_pressed()[0] == 1:
                        self.action[i](*self.parameters[i])

class Beranda:
    def __init__(self, screen, screen_width, screen_height, window_size):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_size = window_size
        self.path = "Beranda"
        self.battle = None
        self.buttons = gp.pygame.sprite.Group()
        self.set_background = self.func_set_background("../resources/assets/Menu/home.png", self.window_size)

    def add_button(self, image, pos_x, pos_y, action=None, parameters=[]):
        button = Button(image, pos_x, pos_y, action, parameters)
        self.buttons.add(button)

    def views_menu_lvl(self):
        gp.pygame.draw.rect(self.screen, 'silver', (self.screen_width // 6 + 400, self.screen_height // 6, self.screen_width // 1.5 - 400, self.screen_height // 1.5 + 100), border_radius=10)
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 2, self.screen_height // 2 - 160, action=[self.set_path], parameters=[["Battle"]])
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 2, self.screen_height // 2 - 70, action=[self.set_path], parameters=[["Battle"]])
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 2, self.screen_height // 2 + 20, action=[self.set_path], parameters=[["Battle"]])
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 2, self.screen_height // 2 + 260, action=[self.set_path], parameters=[["Beranda"]])

    def views_Beranda(self):
        self.add_button(load_image("../resources/assets/Menu/start_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 - 150, action=[self.set_path, self.set_Level], parameters=[["Battle"],[Level1, [self.screen, self.screen_width, self.screen_height]]])
        self.add_button(load_image("../resources/assets/Menu/inventory_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 + 20)
        self.add_button(load_image("../resources/assets/Menu/exit_button.png"), self.screen_width // 3 + 84, self.screen_height // 2 + 200, action=[gp.pygame.quit, sys.exit])

    def rendering(self, height, width):
        self.screen_height = height
        self.screen_width = width
        self.buttons.empty()        
        self.screen.blit(self.set_background,(0,0))

        if self.path == "Beranda":
            self.views_Beranda()
        elif self.path == "Beranda/Stage":
            self.set_background = self.func_set_background("../resources/assets/level select/level select.png", self.window_size)
            self.views_menu_lvl()
        elif self.path == "Battle":
            self.screen.fill((0, 0, 0)) # Ganti Background nanti klo dah jadi
            self.battle.run()
        else:
            self.views_Beranda()

        self.buttons.update()

        for button in self.buttons:
            if button.rect.collidepoint(gp.pygame.mouse.get_pos()):
                gp.pygame.draw.rect(self.screen, 'cyan', button.rect, border_radius=10)
                if gp.pygame.mouse.get_pressed()[0] == 1:
                    button.handle_click()
            self.screen.blit(button.image, button.rect.topleft)

        for event in gp.pygame.event.get():
            if event.type == gp.pygame.QUIT:
                return False
            elif event.type == gp.pygame.VIDEORESIZE:
                self.screen_width = event.w
                self.screen_height = event.h
                self.set_background = self.func_set_background("../resources/assets/Menu/home.png", self.window_size)
        return True

    def func_set_background(self, file, window_size):
        current_directory = os.path.dirname(os.path.abspath(__file__)) 
        image_path = os.path.join(current_directory, file) 
    
        try:
            image = gp.pygame.image.load(image_path)
            scaled_image = gp.pygame.transform.scale(image, window_size)
            return scaled_image
        except gp.pygame.error as e:
            print(f"Failed to load image: {image_filename}")
            raise e
        

    def set_path(self, path):
        self.path = path
        
    def set_Level(self, Level, parameters):
        self.battle = Level(*parameters)