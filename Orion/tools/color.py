WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
LAVENDER = (230, 230, 250)
TEAL = (0, 128, 128)
MAROON = (128, 0, 0)
VIOLET = (238, 130, 238)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
INDIGO = (75, 0, 130)


import pygame
def gradient(screen,height,width,typeGradien="horiz"):
    if typeGradien != "horiz":
        height,width = width,height
    for y in range(height):
        # Hitung warna gradien berdasarkan posisi y
        r = int(255 * y / height)
        g = 0
        b = int(255 * (1 - y / height))

        # Gambar baris dengan warna gradien
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))


