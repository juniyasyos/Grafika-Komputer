import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

rocket = pygame.transform.scale(pygame.image.load("bullet.png"),(50,50))
rocket_rect = rocket.get_rect()
rocket_x, rocket_y = 100, 100
rocket_speed = 2

target = pygame.transform.scale(pygame.image.load("target.png"),(50,50))
target_rect = target.get_rect()
target_x, target_y = 500, 400

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logika pergerakan roket untuk mengejar target
    dx = target_x - rocket_x
    dy = target_y - rocket_y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance > 0:
        rocket_x += (dx / distance) * rocket_speed
        rocket_y += (dy / distance) * rocket_speed

    screen.fill((255, 255, 255))
    screen.blit(rocket, (rocket_x, rocket_y))
    screen.blit(target, (target_x, target_y))

    pygame.display.flip()

pygame.quit()
