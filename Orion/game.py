import pygame
from icecream import ic
import os
import sys
from graphics.gameplay.menu import Beranda

os.environ['SDL_VIDEO-CENTERED'] = '1'
    
class Game:
    def __init__(self) -> None:
        pygame.init()
        WINDOW_INFO_SIZE = pygame.display.Info()

        #elemen jendela
        self.WIDTH = WINDOW_INFO_SIZE.current_w - 10
        self.HEIGHT = WINDOW_INFO_SIZE.current_h - 60
        self.WINDOW_SIZE = (self.WIDTH, self.HEIGHT)
        self.set_background = self.load_image("graphics", "resources", "assets", "Menu", "home.png")

        # navigasi keyboard jendela
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,pygame.RESIZABLE)
        pygame.display.set_caption("Orion")
        self.font = pygame.font.Font(None, 24)
        self.mainMenu = Beranda(self.screen, self.WIDTH, self.HEIGHT, background=self.set_background.convert())
    
    def rendering(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.blit(self.set_background, (0, 0))
            running = self.mainMenu.rendering(height=self.HEIGHT, width=self.WIDTH)
            clock.tick(60)

            text = self.font.render(f"fps: {int(clock.get_fps())}", True, "white")
            self.screen.blit(text, (20, self.HEIGHT-50))
            pygame.display.update()
        pygame.quit()
        sys.exit()

    def load_image(self, *image_filename):
        current_directory = os.getcwd()
        image_path = os.path.join(current_directory, *image_filename)

        try:
            image = pygame.image.load(image_path)
            scaled_image = pygame.transform.scale(image, self.WINDOW_SIZE)
            scaled_image = scaled_image
            return scaled_image
        except pygame.error as e:
            print(f"Failed to load image: {image_filename}")
            raise e

game = Game()
game.rendering()
