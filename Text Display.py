import pygame, sys, time
from pygame.locals import *

pygame.init()
Surface = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Hi peeps')

white = (255, 255, 255)
red = (255, 0, 0)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurface = fontObj.render('GAME OVER!', False, red, (0, 0, 0))
textRect = textSurface.get_rect()
textRect.center = (280, 200)

'''

sound = pygame.mixer.Sound('mp3-now.com - FREE Juice WRLD Type Beat  Last Legs Prod BeatsbyAdz.mp3')
sound.play()

time.sleep(100)
pygame.mixer.music.stop()
pygame.mixer.init()
'''

while True:
    Surface.fill((0, 0, 255))
    Surface.blit(textSurface, textRect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

"""
pygame.mixer.music.load('Nardo-Wick-Who-Want-Smoke.mp3')
pygame.mixer.music.play(-1, 2.0)
time.sleep(100)
pygame.mixer.music.stop()
pygame.mixer.init()
"""