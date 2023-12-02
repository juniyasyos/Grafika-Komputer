import pygame

# Inisialisasi Pygame
pygame.init()

# Set up layar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Sound Example")

# Inisialisasi suara
pygame.mixer.init()

# Load sound files
sound_files = {
    pygame.K_a: pygame.mixer.Sound("graphics/resources/assets/Sound/button click.mp3"),
    pygame.K_s: pygame.mixer.Sound("graphics/resources/assets/Sound/win sound.mp3"),
    pygame.K_d: pygame.mixer.Sound("graphics/resources/assets/Sound/battle sound .mp3"),
}

# Inisialisasi font
font = pygame.font.Font(None, 36)

# Fungsi untuk menampilkan teks di layar
def show_text(text, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Memeriksa apakah tombol yang ditekan ada dalam pemetaan suara
            if event.key in sound_files:
                sound_files[event.key].play()

    # Menampilkan teks instruksi
    show_text("Tekan tombol 'A', 'S', atau 'D' untuk mendengar suara!", 100, 50)

    pygame.display.flip()
    clock.tick(60)

# Berhenti pygame
pygame.quit()
