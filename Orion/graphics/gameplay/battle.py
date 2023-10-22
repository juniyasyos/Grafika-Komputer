import pygame
from .player import Player

class Game:
    def __init__(self,screen, screen_width, screen_height):
        self.screen = screen
        self.screen_height = screen_height
        self.screen_width = screen_width

        # Membuat objek Player
        self.player = Player(self.screen_width, self.screen_height, screen=self.screen)

    def run(self):
        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Membersihkan layar dengan warna hitam
        self.screen.fill((0, 0, 0))

        # Gambar kembali objek pemain
        self.player.update(self.screen_width, self.screen_height, self.player.speed)

        # Draw player health bar and score
        self.player.draw_health_bar(self.screen)
        self.player.draw_score(self.screen)

        # Draw countdown cooldown text
        cooldown_text = self.player.font.render(self.player.skill_cooldown_text, True, (255, 255, 255))
        self.screen.blit(cooldown_text, (10, 10))  # Ganti posisi sesuai kebutuhan

        # Update the display
        pygame.display.flip()
        
if __name__ == "__main__":
    game = Game()
    game.run()