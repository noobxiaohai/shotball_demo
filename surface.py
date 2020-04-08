import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
surface = pygame.Surface(screen.get_size())

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # print('drawing')
    # time.sleep(1)
    pygame.draw.rect(screen, (128, 0, 0), (0, 0, 128, 128))
    # screen.blit(surface, (0, 0))
    pygame.display.update()
