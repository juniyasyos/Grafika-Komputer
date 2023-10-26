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
        self.set_background = 'black'
        self.functions = []

        # navigasi keyboard jendela
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,pygame.RESIZABLE)
        pygame.display.set_caption("Orion")
        self.mainMenu = Beranda(self.screen, self.WIDTH, self.HEIGHT)
    
    def rendering(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            #Logic Game
            self.screen.fill(self.set_background)
            self.mainMenu.rendering(color='silver',height=self.HEIGHT,width=self.WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            clock.tick(70)
            pygame.display.update()

            # Cek apa bila fps drop
            if clock.get_fps() < 30:
                ic(clock.get_fps(), clock.get_time())
        pygame.quit()

    def elemenGame(self):
        for func in self.functions:
            func()

    set_function = lambda self,func :self.functions.append(func)


game = Game()
game.rendering()