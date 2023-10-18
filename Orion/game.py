import pygame
import keyboard
import os
from graphics.gameplay.menu import Beranda

os.environ['SDL_VIDEO-CENTERED'] = '1'
class Game:
    def __init__(self) -> None:
        pygame.init()
        WINDOW_INFO_SIZE = pygame.display.Info()

        #elemen jendela
        self.WIDTH = WINDOW_INFO_SIZE.current_w
        self.HEIGHT = WINDOW_INFO_SIZE.current_h
        self.WINDOW_SIZE = (self.WIDTH - 10,self.HEIGHT-50)
        self.set_background = 'black'
        self.functions = []

        # navigasi keyboard jendela
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,pygame.RESIZABLE)
        pygame.display.set_caption("Orion")
        self.mainMenu = Beranda(self.screen)
    
    def rendering(self):
        running = True
        while running:
            #Logic Game
            self.screen.fill(self.set_background)
            self.mainMenu.rendering(color='silver',height=self.HEIGHT,width=self.WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.update()
        pygame.quit()

    def elemenGame(self):
        for func in self.functions:
            func()

    set_function = lambda self,func :self.functions.append(func)
game = Game()
game.rendering()