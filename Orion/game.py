import pygame
from icecream import ic
import os
import sys
from graphics.gameplay.view import Views

os.environ['SDL_VIDEO-CENTERED'] = '1'
    
class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        WINDOW_INFO_SIZE = pygame.display.Info()

        #elemen jendela
        self.WIDTH = WINDOW_INFO_SIZE.current_w - 10
        self.HEIGHT = WINDOW_INFO_SIZE.current_h - 60
        self.WINDOW_SIZE = (self.WIDTH, self.HEIGHT)

        # navigasi keyboard jendela
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,pygame.RESIZABLE)
        pygame.display.set_caption("Orion")
        self.font = pygame.font.Font(None, 24)
        self.Views = Views(self.screen, self.WIDTH, self.HEIGHT, window_size=self.WINDOW_SIZE)
    
    def rendering(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.Views.rendering(height=self.HEIGHT, width=self.WIDTH)
            clock.tick(60)
            text = self.font.render(f"fps: {int(clock.get_fps())}", True, "white")
            self.screen.blit(text, (20, self.HEIGHT-50))
            pygame.display.update()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.rendering()