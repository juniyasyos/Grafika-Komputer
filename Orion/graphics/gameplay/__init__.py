import os
import random
import threading
import pygame

def load_image(image_filename, size=(10,10), rotation=None, colorkey=None, scale=None):
    current_directory = os.path.dirname(os.path.abspath(__file__))  # Mengambil direktori saat ini
    image_path = os.path.join(current_directory, image_filename)  # Membuat jalur lengkap ke file gambar

    try:
        original_image = pygame.image.load(image_path)
        original_image = pygame.transform.scale(original_image, size)  # Mengubah ukuran gambar
        if colorkey is not None:
            original_image.set_colorkey(colorkey)  # Mengatur transparansi berdasarkan colorkey

        if rotation is not None:
            original_image = pygame.transform.rotate(original_image, rotation)  # Memutar gambar

        if scale is not None:
            original_image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale),
                                                                    int(original_image.get_height() * scale)))

        image = original_image.convert_alpha()
        return image
    except pygame.error as e:
        print(f"Failed to load image: {image_filename}")
        raise e