import pygame
import os
import sys
import pygame.freetype
import time


"""
Variables
"""
worldx = 1200 # These worldx and worldy variables could be changed later to accomodate a bigger background
worldy = 720  # Both variables would be changed to accomodate different screen size.

s = 'GameMusic'

fps = 40  # Frame rate
ani = 4  # animation cycles
BLUE = (25, 25, 200)
BLACK = (25, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 0, 0)  # Aplha value for the image is not known yet. Need to download GIMP or something else as a graphic
# application.
main = True
tileX = 287
tileY = 108
forwardx = 700
backwardx = 200


"""
Objects
"""


# The functions here are for the health and score values. These show them on the game screen
# I used these first two functions before when I haven't gotten the font I needed. I won't call them in the main loop.
'''
def stats():
    text = myfont.render('Score: ' + str(player.score), True, (255, 0, 255))
    world.blit(text, (0, 0))


def health_point():
    text = myfont.render('Health: ' + str(player.health), True, BLACK)
    world.blit(text, (0, 50))

def game_over():
    text = myfont.render('Game Over', True, BLUE)
    world.blit(text, (400, 400))
'''

# Main function that displays health and score.
def stats(score, health):
    font.render_to(world, (4, 4), 'Score: ' + str(score), BLACK, None, size=24)
    font.render_to(world, (4, 45), 'Health: ' + str(health), BLACK, None, size=24)

def lose():
    font.render_to(world, (400, 400), 'Game Over', BLACK, None, size=64)

def win():
    font.render_to(world, (400, 50), 'You win!', BLACK, None, size=64)


# Create platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, xLocation, yLocation, imgWidth, imgHeight, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('GameImages', img)).convert()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = yLocation
        self.rect.x = xLocation


# Create the player class


class Player(pygame.sprite.Sprite):
    # Spawn a player

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # This tracks movement
        self.movex = 0  # Move along x axis
        self.movey = 0  # Move along y axis
        self.frame = 0  # Counts the frames
        self.health = 20
        self.damage = 0
        self.damage2 = 0
        self.score = 0
        self.is_jumping = True
        self.is_falling = False
        self.facing_right = True
        self.images = []

        # I need to animate the character, but for now, I will it as a whole 'boring' character. I can do this
        # by editing and adding " + str(1) + '.png'" to the line below.
        # And also, I added a for loop to iterate through the image 4 times.
        for i in range(1, 5):
            img = pygame.image.load(os.path.join('GameImages', 'cattie1.png')).convert()
            img.convert_alpha()  # This helps to eliminate visble boxes around the image.
            img.set_colorkey(ALPHA)  # Set your alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()


    def control(self, x, y):
        # Controls a player's movement
        self.movex += x
        self.movey += y

    def update(self):
        # Updates the sprite's position


        # There might be a change in the future to this code but I need to remember to change the position
        # of the transform.flip
        # function depending on the direction the image is using.
        # If I want it to turn to the right if it's originally made to look left, I add the transform to the
        # turn right code block.
        # If it is looking right originally but want to change its direction on keypress to move left,
        # I add the transform to the
        # move left code block

        # Added the pygame.transform.flip to the move left code since I've been able to make the image look right
        # as I wanted.
        # Edited with Paint 3D.
        # Moving left
        if self.movex < 0:
            self.is_jumping = True  # Makes the player get down from a platform or reactivates gravity after seeing
            # no collision between platform and the player
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # Removed the pygame.transform.flip function from here since the image has been altered to look right from
        # the start.
        # Moving right
        if self.movex > 0:
            self.is_jumping = True  # Makes the player get down from a platform or reactivates gravity after seeing
            # no collision between platform and the player
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[self.frame // ani]

        # Checks for collision between enemy and player and removes 1 from player's health for each collision.
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        '''
        for hit in hit_list:
            self.health -= 1
            # print(self.health)
        '''

        # Fix the health counter going way down too much.
        if self.damage == 0:
            for enemy in hit_list:
                pygame.mixer.Sound.play(enemySound)
                if not self.rect.contains(enemy):
                    self.damage = self.rect.colliderect(enemy)

        if self.damage == 1:
            idx = self.rect.collidelist(hit_list)
            if idx == -1:
                global main
                self.damage = 0
                self.health -= 1
                if self.health == 0:
                    main = False
                    # game_over()


        hit_list2 = pygame.sprite.spritecollide(self, enemy_list2, False)
        '''
        for hit in hit_list2:
            self.health -= 1
            print('Health is ' + str(self.health))
        '''

        # Checks for collision between enemy and player and substracts health points
        # for collision.
        # Also, reads each collision between enemy and player as one not as before which goes
        # way down

        if self.damage2 == 0:
            for enemy2 in hit_list2:
                pygame.mixer.Sound.play(enemySound)
                if not self.rect.contains(enemy2):
                    self.damage2 = self.rect.colliderect(enemy2)

        if self.damage2 == 1:
            idx = self.rect.collidelist(hit_list2)
            if idx == -1:
                self.damage2 = 0
                self.health -= 1


        # Checks for collision between the player and the ground and then set the bottom of the player to the top to
        # create the illusion of standing on the ground.
        # It also sets self.is_falling to 0 to know that the player is not jumping.
        # And also sets the self.movey to 0 so that the player is not pulled by gravity.
        ground_hit_list = pygame.sprite.spritecollide(self, ground_list2, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_jumping = False


        # Ain't implemented for now.
        # Penalty for falling off the game world.
        if self.rect.y > worldy:
            self.health -= 1
            print(self.health)
            self.rect.x = tileX
            self.rect.y = tileY

        # Detects collision between player and loot and rewards the player and then remove the loot from screen.
        loot_hit_list = pygame.sprite.spritecollide(self, loot_list, False)
        for loot in loot_hit_list:
            loot_list.remove(loot)
            self.score += 1
            # print(self.score)


        # Checks for collision between the platform and the player
        # It sets the self.is_jumping to False if it detects a collision between the player and platform
        # and sets the position of the player to 0 to stop it from moving elsewhere
        plat_hit_list = pygame.sprite.spritecollide(self, plat_list2, False)
        for p in plat_hit_list:
            self.is_jumping = False
            self.movey = 0

            # Checks if the position of the bottom of the player is less than that of the platform, if so,
            # it makes the player land on it. Else, it drops the player away from underneath it.
            if self.rect.bottom <= p.rect.bottom:
                self.rect.bottom = p.rect.top
            else:
                self.movey += 2

        # If self.is_jumping is True and self.is_falling is False, raise the player 33 pixels in the 'air'
        # It also sets is_falling to True to prevent another jump. If set to False, it would shoot the player into the
        # outside the game world.
        if self.is_jumping and self.is_falling is False:
            self.is_falling = True
            self.movey -= 20  # How high to jump

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

    # Controlled from the update function.
    def jump(self):
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True


    def gravity(self):
        if self.is_jumping:
            self.movey += 1.5  # The rate at whicn the player falls.

    # def win(self):
        # if self.score == 4:
            # main = False
            # print('You win')
            # main = False

        # if self.health == 0:
            # main = False

        '''
        if self.rect.y > worldy and self.movey >= 0:
            self.movey = 0
            self.rect.y = worldy - tileY - tileY
        '''

# Create the enemy class


class Enemy(pygame.sprite.Sprite):
    # Spawn enemy
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('GameImages', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0  # counter variable that checks the paces of an enemy or its position

    def move(self):
        # enemy movement
        distance = 80
        speed = 4

        # Removed the PyCharm simplification code to an understandable one
        # Simplification of the if-else code by Pycharm  <Ignore>
        # Original code is;

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0
        self.counter += 1

    def gravity(self):
        self.movey += 0.5  # The rate at whicn the player falls.

        if self.rect.y > worldy and self.movey >= 0:
            self.movey = 0
            self.rect.y = worldy - tileY

    def update(self, firepower, enemy_list):
        # Detect collision
        fire_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fire_hit_list:
            enemy_list.remove(self)
            fire.remove(firepower)
            player.score += 1


class Enemy2(pygame.sprite.Sprite):
    # Spawn second enemy
    # Not the best hack in my opinion but I will go for this now and can fix it later on when I learn more
    # about classes.
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('GameImages', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0


    def enMove2(self):
        distance = 50
        speed = 3

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0
        self.counter += 1


    def update(self, firepower, enemy_list2):
        # Detect collision
        fire_hit_list = pygame.sprite.spritecollide(self, firepower, False)
        for fire in fire_hit_list:
            enemy_list2.remove(self)
            fire.remove(firepower)
            player.score += 1

    # Not yet implemented for now cos I don't really understand why it is not working.
    '''
    def gravity(self):
        self.movey += 0.5  # The rate at whicn the enemy falls.

        if self.rect.y > worldy and self.movey >= 0:
            self.movey = 0
            self.rect.y = worldy - tileY
    '''

# Create levels


class Level:


    # The commented code below is for an hand-painted platform or ground method
    # Gonna implement the tile method and see the better or easiest.

    '''
    def ground1(lvl, x, y, w, h):
        ground_list1 = pygame.sprite.Group()
        if lvl == 1:
            ground1 = Platform(x, y, w, h, 'ground2.png')
            ground_list1.add(ground1)

        if lvl == 2:
            print('Level ' + str(lvl))

        return ground_list1
    '''

    """
    def platform1(lvl):
        plat_list1 = pygame.sprite.Group()
        if lvl == 1:
            # Still don't understand this line yet and the third one from it. Prolly gon' change the values
            # to something I understand.
            plat = Platform(4500, 300, 0, 67, 'platform2.png')
            plat_list1.add(plat)

        return plat_list1
    """

    '''
            plat = Platform(600, 400, 0, 54, 'platform2.png')
            plat_list1.add(plat)
            plat = Platform(800, 300, 0, 54, 'platform2.png')
            plat_list1.add(plat)
            plat = Platform(1000, 200, 0, 54, 'platform2.png')
            plat_list1.add(plat)
            plat = Platform(1500, 550, 0, 54, 'platform2.png')
            plat_list1.add(plat)
    '''


    # The tile method of platform or ground making.
    def ground2(lvl, groundLocation2, tileX, tileY):
        ground_list2 = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(groundLocation2):
                ground2 = Platform(groundLocation2[i], worldy - tileY, tileX, tileY, 'ground2.png')
                ground_list2.add(ground2)
                i += 1

        if lvl == 2:
            print('Level ' + str(lvl))

        return ground_list2

    def platform2(lvl, tileX, tileY):
        plat_list2 = pygame.sprite.Group()
        platLocation = []
        i = 0
        if lvl == 1:
            platLocation.append((200, worldy - tileY - 216, 2))
            platLocation.append((300, worldy - tileY - 432, 3))
            # platLocation.append((500, worldy - tileY - 216, 2))
            platLocation.append((1800, worldy - tileY - 400, 2))
            platLocation.append((1900, worldy - tileY - 200, 2))
            platLocation.append((2900, worldy - tileY - 380, 2))
            platLocation.append((4000, worldy - tileY - 500, 2))
            platLocation.append((5000, worldy - tileY - 380, 2))
            platLocation.append((6000, worldy - tileY - 500, 2))



            while i < len(platLocation):
                j = 0
                while j <= platLocation[i][2]:
                    plat = Platform((platLocation[i][0] + (j*tileX)), platLocation[i][1], tileX, tileY, 'platform2.png')
                    plat_list2.add(plat)
                    # plat2 = Platform((7000, 512, 43, 100, 'VerticalPlat1.png'))
                    # plat_list2.add(plat2)
                    j += 1
                # print('Run ' + str(i) + str(platLocation[i]))
                i += 1

        if lvl == 2:
            print('Level ' + str(lvl))

        return plat_list2


    # Commented out because I don't have the required loot graphic.

    def loot(lvl):
        if lvl == 1:
            loot_list = pygame.sprite.Group()
            loot = Platform(800, 400, 40, 40, 'gem.png')  # The values here will probably change
            # depending on the graphic used.
            loot2 = Platform(2000, 300, 40, 40, 'bag.png')
            loot3 = Platform(3000, 200, 40, 40, 'gem.png')
            loot_list.add(loot, loot2, loot3)

        if lvl == 2:
            print('Loot for level ' + str(lvl))

        return loot_list



    def bad(lvl, enemyLocation):
        if lvl == 1:
            enemy = Enemy(enemyLocation[0], enemyLocation[1], 'space-invaders.png')
            en2 = Enemy(enemyLocation[2], enemyLocation[3], 'space-invaders.png')
            en3 = Enemy(enemyLocation[4], enemyLocation[5], 'space-invaders.png')
            en4 = Enemy(enemyLocation[6], enemyLocation[7], 'space-invaders.png')
            en5 = Enemy(enemyLocation[8], enemyLocation[9], 'space-invaders.png')
            en6 = Enemy(enemyLocation[10], enemyLocation[11], 'space-invaders.png')
            en7 = Enemy(enemyLocation[12], enemyLocation[13], 'space-invaders.png')
            en8 = Enemy(enemyLocation[14], enemyLocation[15], 'space-invaders.png')
            en9 = Enemy(enemyLocation[16], enemyLocation[17], 'space-invaders.png')

            enemy_list = pygame.sprite.Group()
            # enemy_list.add(enemy)
            # enemy_list.add(en2)
            enemy_list.add(enemy, en2, en3, en4, en5, en6, en7, en8, en9)

        if lvl == 2:
            print('Level ' + str(lvl))

        return enemy_list

    def bad2(lvl, enemyLocation_2):
        if lvl == 1:
            enemy2 = Enemy2(enemyLocation_2[0], enemyLocation_2[1], 'Tutorialenemy.png')
            enemy2_1 = Enemy2(enemyLocation_2[2], enemyLocation_2[3], 'Tutorialenemy.png')
            enemy2_2 = Enemy2(enemyLocation_2[4], enemyLocation_2[5], 'Tutorialenemy.png')
            enemy2_3 = Enemy2(enemyLocation_2[6], enemyLocation_2[7], 'Tutorialenemy.png')
            enemy2_4 = Enemy2(enemyLocation_2[8], enemyLocation_2[9], 'Tutorialenemy.png')
            enemy2_5 = Enemy2(enemyLocation_2[10], enemyLocation_2[11], 'Tutorialenemy.png')
            enemy2_6 = Enemy2(enemyLocation_2[12], enemyLocation_2[13], 'Tutorialenemy.png')
            enemy2_7 = Enemy2(enemyLocation_2[14], enemyLocation_2[15], 'Tutorialenemy.png')
            enemy2_8 = Enemy2(enemyLocation_2[16], enemyLocation_2[17], 'Tutorialenemy.png')

            enemy_list2 = pygame.sprite.Group()
            # enemy_list2.add(enemy2)
            enemy_list2.add(enemy2, enemy2_1, enemy2_2, enemy2_3, enemy2_4, enemy2_5, enemy2_6, enemy2_7, enemy2_8)
            # enemy_list2.add(enemy2_2)

        if lvl == 2:
            print('Level ' + str(lvl))

        return enemy_list2


class Throwable(pygame.sprite.Sprite):
    def __init__(self, x, y, img, throw):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('GameImages', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.firing = throw
        self.thrown = True
        # self.rect.x = 0
        # rightDir = self.rect.x + 20
        # leftDir = self.rect.x - 20

    # I've been trying to implement some checks here to make sure that the bullet shot forward does'nt
    # come backward when the player changes direction. But to no avail yet. Prolly gon' leave it until I find a fix. :(
    def update(self, worldx):
        # Throw physics
        if self.rect.x < worldx:
            if player.facing_right:
                self.rect.x += 50
                '''
                if self.rect.x == 50:
                    self.kill()
                    self.firing = 0
                '''

                # self.firing = 0

                if self.rect.x >= worldx:
                    self.kill()
                    self.firing = 0

                # self.rect.y += 5
            if not player.facing_right:
                fire.remove(firepower)
                # self.firing = 0
                # self.kill()

                self.rect.x -= 50
                fire.add(firepower)

                if self.rect.x <= 0:
                    self.kill()
                    self.firing = 0
            # self.rect.y += 5

        else:
            self.kill()
            self.firing = 0


"""
Setup
"""

# Contains our setup code blocks. These help with things that build the basis for the game
clock = pygame.time.Clock()
pygame.init()  # Essential to create the game framework
pygame.mixer.init()  # For sound
bulletSound = pygame.mixer.Sound(os.path.join(s, 'laserRetro.ogg'))
enemySound = pygame.mixer.Sound(os.path.join(s, 'Impact.ogg'))


backSound = pygame.mixer.music.load(os.path.join(s, 'sound3.ogg'))
pygame.mixer.music.play(-1)

world = pygame.display.set_mode([worldx, worldy])
# I wanna change the game's background to include a color instead of a shitty background until I get a better graphic.
backdrop = pygame.image.load(os.path.join('GameImages', 'shore.jpg'))
# Copied Ursina's game engine default sky to my working directory to use as a background for now.
# Ignore the comment above backdrop variable for now.
pygame.display.set_caption('Ghoul Hunter')
icon = pygame.image.load(os.path.join('GameImages', 'cattie1.png'))
pygame.display.set_icon(icon)
backdropbox = world.get_rect()

# Call the player class
player = Player()  # Spawn the player
player.rect.x = 0  # Go to a place x
player.rect.y = 0  # Go to a place y or this means be in this particular position for y axis and x above
# Note that in the game world, x axis increases to the right from the top left
# Y axis increases downward from the top.
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10  # the number of pixels to move

fire = Throwable(player.rect.x, player.rect.y, 'bullet.png', 0)
firepower = pygame.sprite.Group()

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Assets', 'Mini Square Mono.ttf')
font_size = 24
pygame.freetype.init()
font = pygame.freetype.Font(font_path, font_size)

# Enemy's location and call to the Level.bad method to define levels and position you want enemy to spawn.
# enemyLocation = []
enemyLocation = [300, 120, 500, 340, 2900, 558, 4000, 500, 4200, 350, 6000, 230, 4800, 490, 2300, 440, 7000, 450]
# This is the position of one enemy for now, it would probably change
# to accomodate updates to code. This contains the list of three enemy positions but due to an ingenious hack, I've
# broken them into imdividual lists leaving the original above.

enemyLocation3 = [300, 558]  # Position of third enemy yet to be implemented.

enemyLocation_2 = [200, 320, 1200, 500, 2000, 300, 3200, 500, 4000, 300, 5000, 512, 5200, 439, 5700, 400, 6600, 300]
# Position of second enemy

# noinspection PyTypeChecker
enemy_list = Level.bad(1, enemyLocation)

# noinspection PyTypeChecker
enemy_list2 = Level.bad2(1, enemyLocation_2)

# Call the ground and platform functions in hand-painted method
# noinspection PyTypeChecker
# ground_list1 = Level.ground1(1, 0, 650, 1125, 205)
# noinspection PyTypeChecker
# plat_list1 = Level.platform1(1)

loot_list = Level.loot(1)  # Function call for loots

# Gonna change when I download the main font type in the tutorial.
# myfont = pygame.font.Font('freesansbold.ttf', 32)
# No need as I have downloaded the font I need.


# Commented out this to inspect where my different enemy code is going wrong.

# The tile method.
groundLocation2 = []
# tileX = 287
# tileY = 108

i = 0
while i <= (worldx/tileX) + tileX:
    groundLocation2.append(i * tileX)
    i += 1

ground_list2 = Level.ground2(1, groundLocation2, tileX, tileY)
plat_list2 = Level.platform2(1, tileX, tileY)


'''
# Call the enemy class with where you want it to appear on the game along with the image to use
# enemy = Enemy(300, 0, 'enemyship.png')
# enemy_list = pygame.sprite.Group()
# enemy_list.add(enemy)
# Code moved into a new function under a class
'''


"""
Main Loop
"""

while main:

    # The event code below checks for key presses which control the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            '''
            if event.key == ord('q'):
                # pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            '''

            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.jump()
            if event.key == pygame.K_SPACE:
                if not fire.firing:
                    fire = Throwable(player.rect.x, player.rect.y, 'bullet.png', 1)
                    firepower.add(fire)
                    pygame.mixer.Sound.play(bulletSound)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
                player.facing_right = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
                player.facing_right = True

    # scroll the game forward or backward

    # Although counter-intuitive in my opinion, it's really crazy.
    # If the position of the player is 660, and the forwardx variable value is 630
    # Remove forwardx from player's position, that gives 30, deduct it from the position of the platform and the
    # platform's position changes because the new value of its position is becoming smaller on the x-axis
    # giving an illusion of scrolling in the game.

    if player.rect.x >= forwardx:
        scroll = player.rect.x - forwardx
        player.rect.x = forwardx
        for p in plat_list2:
            p.rect.x -= scroll

        for e in enemy_list:
            e.rect.x -= scroll

        for e in enemy_list2:
            e.rect.x -= scroll

        for l in loot_list:
            l.rect.x -= scroll


    # As applied to the forward code block, the player's postion value is deducted from the backwardx value
    # if the position is lesses than the value in backwardx. Add this value to the position of platform on the x-axis
    # makes the position of the platform to be increasing giving the illusion of the player going backward.
    if player.rect.x <= backwardx:
        scroll = backwardx - player.rect.x
        player.rect.x = backwardx
        if player.rect.x == 0:
            player.rect.x = 0

        for p in plat_list2:
            p.rect.x += scroll

        for e in enemy_list:
            e.rect.x += scroll

        for e in enemy_list2:
            e.rect.x += scroll

        for l in loot_list:
            l.rect.x += scroll


    # Changed the game to use a color instead of a graphical background.
    world.blit(backdrop, backdropbox)
    # world.fill(BLUE)
    player.update()  # This updates the player's position and makes the sprite move.
    player.gravity()

    # Since the player's score can't be 20 for now, this won't run.
    if player.score == 20 and player.health != 0:
        win()
        # player.kill()
        # main = False
        # print('You win!')
        # sys.exit()

    # I want to check for when the health of a player depletes and the player hasn't finished the game yet
    # If so, display a Game Over and end the game but I want it to stay long enough for the player to see it and not be
    # like a crash. I think I need to check the Pygame documentation to see if there's something regarding a pause or
    # so that could be implemented.
    if player.health == 0 and player.score < 20:
        lose()
        main = False

        # time.sleep(100)
        # print('You lose')
        # sys.exit()

    # enemy_list.gravity()  # Wanna add gravity to the enemies but don't understand why it's not working yet.
    # enemy2.gravity()
    player_list.draw(world)  # This draws the player onto the screen

    if fire.firing:
        fire.update(worldx)
        firepower.draw(world)
        enemy_list.update(firepower, enemy_list)
        enemy_list2.update(firepower, enemy_list2)

    enemy_list.draw(world)  # Draws the first type of enemy onto the screen
    enemy_list2.draw(world)  # Draws the second type of enemy onto the screen.
    ground_list2.draw(world)  # Draws the ground onto the screen for every loop

    plat_list2.draw(world)  # Draws the platform onto the screen for every loop
    # plat_list1.draw(world)
    loot_list.draw(world)  # Draws the loot onto the screen.
    # stats()
    stats(player.score, player.health)
    # health_point()
    # game_over()

    # Make the enemy move left to right or vice versa forever
    for e in enemy_list:
        e.move()
    for e_2 in enemy_list2:
        e_2.enMove2()
        # e.enMove3()
    pygame.display.flip()
    clock.tick(fps)
