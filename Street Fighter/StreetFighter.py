import sys, pygame
pygame.init()

Screen_w = 1000
Screen_h = 600

screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Street Fighter")

bg = pygame.image.load("")

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()


pygame.quit()