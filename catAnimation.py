import pygame, sys
from pygame.locals import *

pygame.init()

fps = 30
fpsclock = pygame.time.Clock()

Surface = pygame.display.set_mode((400, 300),0, 32)
pygame.display.set_caption('Animation')

color = (98, 67, 109)
catImg = pygame.image.load('catImage.png')
icon = pygame.image.load('catImage.png')
pygame.display.set_icon(icon)
catx = 10
caty = 10
direction = 'right'


while True:
    Surface.fill(color)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'

    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'

    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'

    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    Surface.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsclock.tick(fps)
