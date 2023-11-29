import pygame, sys

from pygame.locals import *

pygame.init()
Surface = pygame.display.set_mode((500, 400))
#rectangle = pygame.Rect(10, 20, 200, 300)
#surface2 = Surface.convert_alpha()
pygame.display.set_caption('Hello World')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

Surface.fill(white)
pygame.draw.polygon(Surface, green, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(Surface, blue, (60, 60), (120, 60), 4)
pygame.draw.line(Surface, blue, (120, 60), (60, 120))
pygame.draw.line(Surface, blue, (60, 120), (120, 120),4)
pygame.draw.circle(Surface, blue, (300, 50), 20, 0)
pygame.draw.ellipse(Surface, red, (300, 250, 40, 80), 1)
pygame.draw.rect(Surface, red, (200, 150, 100, 50))

"""
pixObj = pygame.PixelArray(Surface)
pixObj[480][380] = black
pixObj[482][382] = black
pixObj[484][384] = black
pixObj[486][386] = black
pixObj[488][388] = black
del pixObj
"""




while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
