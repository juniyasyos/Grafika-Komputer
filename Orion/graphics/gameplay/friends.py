import pygame
import gameplay as gp  

class Friend(pygame.sprite.Sprite):
    def _init_(self, screen, player, enemies, friend_bullets):
        super()._init_()

       
        self.image = gp.load_image("path_to_friend_ship_image.png", size=(50, 50), colorkey=("white"))
        self.rect = self.image.get_rect()

        # Set posisi awal teman di sebelah pesawat player
        self.rect.centerx = player.rect.centerx + 50
        self.rect.centery = player.rect.centery

        # Set atribut lainnya
        self.screen = screen
        self.player = player
        self.enemies = enemies
        self.friend_bullets = friend_bullets
        self.shooting = False
        self.shoot_duration = 5000  # Waktu durasi menembak teman dalam milidetik
        self.last_shoot_time = 0

    def update(self):
       
        if self.shooting:
            self.rect.x += 5 

            # Tembak musuh selama durasi menembak
            if pygame.time.get_ticks() - self.last_shoot_time < self.shoot_duration:
                self.shoot()
            else:
                self.shooting = False
                self.kill()  # Hapus pesawat teman setelah durasi menembak berakhir

    def shoot(self):
     

        
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                # Tambahkan tembakan ke musuh (sesuai logika game Anda)
                bullet = FriendBullet(self.screen, self.rect.center, enemy.rect.center)
                self.friend_bullets.add(bullet)

class FriendBullet(pygame.sprite.Sprite):
    def _init_(self, screen, friend_position, enemy_position):
        super()._init_()

        # Load image tembakan teman
        self.image = gp.load_image("path_to_friend_bullet_image.png", size=(10, 10), colorkey=("white"))
        self.rect = self.image.get_rect()

        # Set posisi tembakan teman
        self.rect.center = friend_position

        # Tentukan kecepatan tembakan teman (sesuai kebutuhan)
        self.speed = 8

        # Tentukan arah tembakan teman menuju musuh
        self.direction = gp.get_direction(friend_position, enemy_position)

    def update(self):
        # Perbarui posisi tembakan teman
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Hapus tembakan teman jika telah mencapai batas layar atau musuh
        if self.rect.x < 0 or self.rect.x > gp.SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > gp.SCREEN_HEIGHT:
            self.kill()