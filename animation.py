#Import library 
import pygame
import math
import random

#Define colours
sky_day = (93,148,251)
sky_night = (172,93,251)

#Define screen size
width = 700
height = 500

#Define entity class for all moving objects
class Entity:
    x = 0
    y = 0
    speed = 0
    image = ""
    isFall = False

    #The initial function 
    def __init__(self,x:int,y:int,speed:int,image:pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image
    
    #Move any object forward
    def forward(self) -> None:
        self.gesture = round(frames / 9 % 3)
        self.x = self.x + self.speed
    
    #Print any object on the screen
    def draw(self) -> None:
        screen.blit(self.image,(self.x,self.y))

#Define character class for objects with animations and seperate movements, inherit from entity class
class Character(Entity):
    #The list holds all animation images
    images = []

    #Current image on display
    gesture = 5

    #Variable name is used for loading corresponding images
    name = ""

    def __init__(self,name:str,x:int,y:int,speed:int,gestures:int) -> None:
        for i in range(1,gestures):
            self.images.append(pygame.image.load("%s.png"%(name + "_" + str(i))))
        self.x = x
        self.y = y
        self.speed = speed
        self.name = name
    
    #Overwrite draw function to display different animations
    def draw(self) -> None:
        screen.blit(self.images[self.gesture],(self.x,self.y))
    
    def jump(self) -> None:
        self.y -= self.speed
        self.gesture = 4
    
    def fall(self) -> None:
        self.y += self.speed
        self.gesture = 3
    
#Define Block class for random blocks and bricks
class Block(Entity):
    broken = False
    def touch(self):
        if not self.broken:
            self.broken = True
        else:
            if self.y > 200 and not self.isFall:
                self.y -= 10
            elif self.y < 250:
                self.isFall = True
                self.image = blank_img
                self.y += 10

class Enemy(Entity):
    dead = False
    def touch(self):
        if not self.dead:
            self.dead = True
        else:
            if self.y > 300 and not self.isFall:
                self.y -= 10
            elif self.y < 500:
                self.isFall = True
                self.y += 20

#Define a function to generate random clouds
def generate_cloud() -> Entity:
    #Generate random position and speed for a cloud entity
    x = random.randint(-200,-50)
    y = random.randint(0,300)
    speed = random.uniform(1,2)
    #print("[Debug] Generated cloud at ({0},{1}) speed = {2}".format(x,y,speed))
    return Entity(x,y,speed,cloud_img)

#Initialize Pygame
pygame.init()

#Set the width and height of the screen
size = (width,height)
screen = pygame.display.set_mode(size)

#Set the title of the window
pygame.display.set_caption("[Yichen Wang] Pygame - Super Mario Demo")

#Loop until the user clicks the close button
done = False

#Manage how fast the screen updates
clock = pygame.time.Clock()

#import the images
sun_img = pygame.image.load("sun.png")
moon_img = pygame.image.load("moon.png")
ground_img = pygame.image.load("ground.png")
cloud_img = pygame.image.load("cloud.png")
cloud_night_img = pygame.image.load("cloud_night.png")
brick_img = pygame.image.load("brick.png")
block_img = pygame.image.load("block.png")
blank_img = pygame.image.load("block_blank.png")
monster_img = pygame.image.load("monster.png")
flag_img = pygame.image.load("flag.png")
pod_img = pygame.image.load("pod.png")
end_img = pygame.image.load("end.png")

#Initialize the Mario Character
mario = Character("Mario",0,350,3,7)

#Initialize the clouds list with random clouds
clouds = []
for i in range(10):
    clouds.append(generate_cloud())

#Initialize the blocks
blocks = []
for i in range(3):
    blocks.append(Block(50 + 50*i,250,0,brick_img))
blocks.append(Block(200,250,0,block_img))
for i in range(3):
    blocks.append(Block(250 + 50*i,250,0,brick_img))
blocks.append(Block(400,250,0,block_img))

#Initialize the monster entity
monsters = []

#Initialze the flag entity
flag = Entity(600,50,0,flag_img)
pod = Entity(570,15,0,pod_img)

#Initialize the sun entity
sun = Entity(0,0,1,sun_img)
isDay = True

#Initialize the End Title
end = Entity(170,600,0,end_img)

#The color for the sky
sky = sky_day

#Counter of frames
frames = 0

#Stage of a scene
stage = 0

#Index of scene
scene = 0

#Main Program Loop
while not done:
    #Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #If user clicks close, it will end the main loop.

    #Set the screen
    screen.fill(sky)

    #Drawing code here

    #Sun control
    sun.forward()
    sun.y = height - (width * sun.x - sun.x ** 2) ** 0.5 - 100
    #print("[Debug] The position of sun is ({0},{1})".format(sun.x,sun.y))
    if sun.x > width:
        sun.x = 0
        #Day and Night switch
        isDay = not isDay
        if isDay:
            print("[Debug] It's daytime now!")
            sky = sky_day
            sun.image = sun_img
        else:
            print("[Debug] It's night now!")
            sky = sky_night
            sun.image = moon_img
    else:
        sun.draw()

    #Draw the ground
    screen.blit(ground_img,(0,412))

    #Cloud control
    for cloud in clouds:
        #The color of the clouds change with the day and night
        if isDay:
            cloud.image = cloud_img
        else:
            cloud.image = cloud_night_img
        
        #Draw and move the cloud
        cloud.draw()
        cloud.forward()

        #Regenerate another cloud when one gets to the edge of the screen
        if cloud.x > width:
            clouds.remove(cloud)
            del cloud
            clouds.append(generate_cloud())
            continue
    
    #Block Control
    for block in blocks:
        block.draw()

    #Monster Control
    for monster in monsters:
        monster.draw()

    #Flag Control
    if scene == 3:
        flag.draw()
        pod.draw()

    #Mario control

    #Draw Mario
    mario.draw()

    #Mario Movement Stage 0
    if stage == 0:
        if mario.x < 200:
            mario.forward()
        elif scene == 0:
            if mario.y > 300 and not mario.isFall:
                #jump to break the block
                mario.jump()
            elif mario.y < 350:
                mario.isFall = True
                blocks[3].touch()
                mario.fall()
            else:
                mario.gesture = 5
                stage = 1
                mario.isFall = False
        elif scene == 1:
            if mario.y > 300 and not mario.isFall:
                #jump to break the block
                mario.jump()
            elif mario.y < 300:
                mario.isFall = True
                mario.fall()
            else:
                mario.gesture = 5
                stage = 1
                mario.isFall = False
        else:
            if mario.y > 300 and not mario.isFall:
                #jump to break the block
                mario.jump()
                mario.forward()
            elif mario.y < 350:
                mario.isFall = True
                mario.fall()
                monsters[0].touch()
            else:
                mario.gesture = 5
                stage = 1
                mario.isFall = False
    #Mario Movement Stage 1
    if stage == 1:
        if scene == 2 or scene == 3:
            if mario.x < 400:
                mario.forward()
            elif mario.y > 300 and not mario.isFall:
                mario.jump()
                mario.forward()
            elif mario.y < 350:
                mario.isFall = True
                mario.fall()
                monsters[1].touch()
            else:
                mario.gesture = 5
                stage = 2
                mario.isFall = False
        else:
            if mario.x < 400:
                mario.forward()
            elif mario.y > 300 and not mario.isFall:
                mario.jump()
            elif mario.y < 350:
                mario.isFall = True
                if scene == 0:
                    blocks[7].touch()
                mario.fall()
            else:
                mario.gesture = 5
                stage = 2
                mario.isFall = False
    #Mario Movement Stage 2
    if stage == 2:
        if mario.x < 600:
            mario.forward()
        else:
            if scene == 3:
                mario.speed = 7
                if mario.y > 50 and not mario.isFall:
                    mario.jump()
                elif mario.y < 350:
                    mario.isFall = True
                    mario.fall()
                    flag.y += 6
                else:
                    mario.gesture = 5
                    if end.y > 100:
                        end.y -= 3
                    end.draw()
                    
            else:
                mario.gesture = 5
                stage = 3
                mario.isFall = False
    #Mario Movement Stage 3
    if stage == 3:
        if mario.x < 700:
            mario.forward()
        else:
            mario.x = 0
            stage = 0
            scene += 1
            blocks.clear()
            if scene == 1:
                for i in range(3):
                    blocks.append(Block(250 + 50*i,365,0,brick_img))
            elif scene == 2 or scene == 3:
                monsters.clear()
                for i in range(2):
                    monsters.append(Enemy(250 + 200*i,350,0,monster_img))

    #Update the screen
    pygame.display.flip()

    #update frame counter
    frames += 1

    #Set number of frames per second
    clock.tick(60)

#Close the window and quit
pygame.quit()