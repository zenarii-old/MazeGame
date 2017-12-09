from random import randint, choice
import pygame, sys

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        #Any position in width/length, but a multiple of 30 to fit grid

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect()

        positionNotSet=True
        while positionNotSet:
            self.position=[choice(range(0,width,30)),choice(range(0,height,30))]
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall): print("moved"); continue
            else: break





    def move(self, direction):
        #if collides with wall will move back
        if direction == "up":
            self.position[1] -= tileSize[1]; player.rect.y = player.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[1] += tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "left":
            self.position[0] -= tileSize[0]; player.rect.x = player.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[0] += tileSize[0]
                    self.rect.x = player.position[0]
                    break


        elif direction == "down":
            self.position[1] += tileSize[1]; player.rect.y = player.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[1] -= tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "right":
            self.position[0] += tileSize[0]; player.rect.x = player.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[0] -= tileSize[0]
                    self.rect.x = self.position[0]
                    break


class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.position = [x,y]
        self.image = pygame.Surface(tileSize)
        self.image.fill((100,100,100))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]


class immovableWall(Block, pygame.sprite.Sprite):
    def __init__(self,x,y):
        Block.__init__(self,x,y)
        pygame.sprite.Sprite.__init__(self)

class movableWall(Block, pygame.sprite.Sprite):
    def __init__(self,x,y):
        Block.__init__(self,x,y)
        pygame.sprite.Sprite.__init__(self)

def draw():
    screen.fill((255,255,255))

    screen.blit(player.image,player.position)
    for wall in walls: screen.blit(wall.image, wall.position)

    pygame.display.flip()


tileSize = (30,30)
size = width, height = 810, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Escape the trolls!")
screen.fill((0,0,255))
pygame.display.flip()

upKey = pygame.K_w
leftKey = pygame.K_a
downKey = pygame.K_s
rightKey = pygame.K_d
#----[Wall Generation]----------------------------------------------------------
walls = []
#Generate immovable edge walls (left and right)
for i in range(0,width,tileSize[0]):
    wall = immovableWall(i,0)
    walls.append(wall)
    wall = immovableWall(i,height-tileSize[1]) #to make it on screen
    walls.append(wall)
#Generate immovable edge walls (top and bottom)
for i in range(0,height,tileSize[1]):
    wall = immovableWall(0,i)
    walls.append(wall)
    wall = immovableWall(width-tileSize[0],i) # keeps it on screen
    walls.append(wall)
#----[End Wall Generation]------------------------------------------------------

player = Entity()

while True: #Game loop
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()
        if pressed[upKey]: player.move("up")
        elif pressed[leftKey]: player.move("left")
        elif pressed[downKey]: player.move("down")
        elif pressed[rightKey]: player.move("right")

    draw()
