import pygame
from icecream import ic
import os
from graphics.gameplay.menu import Beranda

os.environ['SDL_VIDEO-CENTERED'] = '1'
    
class Game:
    def __init__(self) -> None:
        pygame.init()
        WINDOW_INFO_SIZE = pygame.display.Info()

        #elemen jendela
        self.WIDTH = WINDOW_INFO_SIZE.current_w - 10
        self.HEIGHT = WINDOW_INFO_SIZE.current_h - 60
        self.WINDOW_SIZE = (self.WIDTH,self.HEIGHT)
        self.set_background = self.load_image("\\graphics\\resources\\assets\\Menu\\home.png")
        self.functions = []

        # navigasi keyboard jendela
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,pygame.RESIZABLE)
        pygame.display.set_caption("Orion")
        self.mainMenu = Beranda(self.screen, self.WIDTH, self.HEIGHT, background=self.set_background)
    
    def rendering(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.blit(self.set_background, (0, 0))
            running = self.mainMenu.rendering(color='silver', height=self.HEIGHT, width=self.WIDTH)

            clock.tick(70)
            pygame.display.update()

    def elemenGame(self):
        for func in self.functions:
            func()


    def load_image(self, image_filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = current_directory + image_filename

        try:
            image = pygame.transform.scale(pygame.image.load(image_path), self.WINDOW_SIZE)
            return image
        except pygame.error as e:
            print(f"Failed to load image: {image_filename}")
            raise e

    set_function = lambda self,func :self.functions.append(func)


game = Game()
game.rendering()