from random import randint, choice
import pygame, sys
import mazeGenerator
from os import path


class Entity(pygame.sprite.Sprite):
    def __init__(self, spriteImage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.rect = self.image.get_rect()
        self.picture = spriteImage
        self.inWall = False
        self.positionNotSet = True

        while self.positionNotSet:
            self.position=[choice(range(0,width,32)),
                           choice(range(0,height,32))]
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            for wall in walls:
                if wall.rect.colliderect(self):break
            else:
                self.positionNotSet = False



    def move(self, direction):
        #if hits with wall will move back
        if direction == "up":
            self.position[1] -= tileSize[1]; self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    wall.push("up")
                    self.position[1] += tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "left":
            self.position[0] -= tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
                    wall.push("left")
                    self.position[0] += tileSize[0]
                    self.rect.x = self.position[0]
                    break


        elif direction == "down":
            self.position[1] += tileSize[1]; self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    wall.push("down")
                    self.position[1] -= tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "right":
            self.position[0] += tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
                    wall.push("right")
                    self.position[0] -= tileSize[0]
                    self.rect.x = self.position[0]
                    break

class Troll(Entity, pygame.sprite.Sprite):
    def __init__(self, color):
        Entity.__init__(self,color)
        pygame.sprite.Sprite.__init__(self)

    def getmoves(self):
        self.canMoveRight = True
        self.canMoveUp = True
        self.canMoveDown = True
        self.canMoveLeft = True

        #checks if can move right
        self.rect.x += tileSize[0]
        for wall in walls:
            if wall.rect.colliderect(self):
                self.canMoveRight = False; break
        self.rect.x = self.position[0]

        #checks to see if can move left
        self.rect.x -= tileSize[0]
        for wall in walls:
            if wall.rect.colliderect(self):
                self.canMoveLeft = False; break
        self.rect.x = self.position[0]
        #checks to see if can move up

        self.rect.y -= tileSize[1]
        for wall in walls:
            if wall.rect.colliderect(self):
                self.canMoveUp = False; break
        self.rect.y = self.position[1]

        #check to see if can move down
        self.rect.y += tileSize[1]
        for wall in walls:
            if wall.rect.colliderect(self):
                self.canMoveDown = False; break
        self.rect.y = self.position[1]

        #adds the possible directions to list then returns it
        directions = []
        if self.canMoveLeft: directions.append("left")
        if self.canMoveRight: directions.append("right")
        if self.canMoveUp: directions.append("up")
        if self.canMoveDown: directions.append("down")
        return directions

    def findPlayer(self):
        """Checks in each direction for 5 blocks, if player is found
        then moves in that direction, if hits wall stops searching.

        Returns None if player isn't found"""
        #in left direction
        wallHit = False
        for i in range(1,6):
            self.rect.x -= tileSize[0]
            if player.rect.colliderect(self): return "left"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in right direction
        wallHit = False
        for i in range(1,6):
            self.rect.x += tileSize[0]
            if player.rect.colliderect(self): return "right"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in up direction
        wallHit = False
        for i in range(1,6):
            self.rect.y -= tileSize[1]
            if player.rect.colliderect(self): return "up"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            if wallHit: break
        self.rect.y = self.position[1]

        #downwards
        for i in range(1,6):
            self.rect.y += tileSize[1]
            if player.rect.colliderect(self): return "down"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            if wallHit: break
        self.rect.y = self.position[1]

    def die(self):
        self.posInList = trolls.index(self)
        trolls.pop(self.posInList)


class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.position = [self.x,self.y]
        self.image = pygame.Surface(tileSize)
        self.image.fill((100,100,100))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
    def smash(self):
        self.positionInList = walls.index(self)
        walls.pop(self.positionInList)


class immovableWall(Block, pygame.sprite.Sprite):
    def __init__(self,x,y):
        Block.__init__(self,x,y)
        pygame.sprite.Sprite.__init__(self)

    def push(self,direction):
        pass

class movableWall(Block, pygame.sprite.Sprite):
    def __init__(self,x,y):
        Block.__init__(self,x,y)
        pygame.sprite.Sprite.__init__(self)

    def push(self, direction):
        if direction == "up":
            self.rect.y -= 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.y += 32; break
            else: self.position[1] = self.rect.y

        elif direction == "left":
            self.rect.x -= 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.x += 32; break
            else: self.position[0] = self.rect.x

        elif direction == "down":
            self.rect.y += 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.y -= 32; break
            else: self.position[1] = self.rect.y

        elif direction == "right":
            self.rect.x += 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.x -= 32; break
            else: self.position[0] = self.rect.x

        for troll in trolls:
            if troll.rect.colliderect(self): troll.die()

class Exit(Block, pygame.sprite.Sprite):
    def __init__(self):
        #self.position = choice("Top")#,"Bottom","Left","Right")
        self.rect = ([32,32],[32,32])
        #if self.position == "Top":
        self.position = [0,0]
        self.position[0] = choice(range(0,width,32))
        self.position[1] = 0

        Block.__init__(self, self.position[0], self.position[1])
        pygame.sprite.Sprite.__init__(self)

        self.image.fill((100,100,100))
        for wall in walls:
            if self.rect.colliderect(wall): wall.smash()

#----[Draw To Screen Function]--------------------------------------------------
def draw():
    screen.fill((0,0,0))

    screen.blit(player.picture,player.position)
    for wall in walls: screen.blit(wallimg, wall.position)
    for troll in trolls: screen.blit(troll.picture, troll.position)
    screen.blit(gate.image, gate.position)
    pygame.display.flip()
#----[End Draw To Screen Function]----------------------------------------------
#As screen may not fit all tiles unexpected behaviour occurs at borders
#this shiould prevent that
def getLength(length):
    lengthRemainder = length % 32
    print(lengthRemainder)
    if lengthRemainder is not 0:
        return length + (32 - lengthRemainder)
    else: return length
#----[Game Setup]---------------------------------------------------------------
tileSize = (32,32)
width, height = 800, 600
width = getLength(width)
height = getLength(height)

size = width,height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Escape the trolls!")

screen.fill((0,0,255))
pygame.display.flip()

BLUE = (10,10,255)
RED = (255,10,10)

upKey = pygame.K_w
leftKey = pygame.K_a
downKey = pygame.K_s
rightKey = pygame.K_d
#----[End Game Setup]-----------------------------------------------------------
#----[Wall Generation]----------------------------------------------------------
mazeString = mazeGenerator.generate(int(width/tileSize[0]/2),
                                    int(height/tileSize[1]/2))
walls = [] #holds all wall objects, immovable or unmovable
mazeList = [] # when string is broken to list each list row is added
mazeRow = [] # each character is the mazeString is added to this


for i in mazeString:
    if i == "\n": mazeList.append(mazeRow); mazeRow = []
    else: mazeRow.append(i)

#TODO, bottom row of walls is movable, need to prevent that
for y in range(len(mazeList)):
    for x in range(len(mazeList[y])):
        #if a wall char make a wall
        if mazeList[y][x] == "+":
            #checks to see if edge wall is being created
            #if it is the wall cannot be moved
            if x == 0 or y == 0:
                wall = immovableWall(x*32,y*32)
            elif x * 32 == width - 32 or y * 32 == height - 32:
                wall = immovableWall(x*32,y*32)
            #Other walls can be moved
            else:
                wall = movableWall(x*32,y*32)
            #adds the wall, whatever type, to the list of walls
            walls.append(wall)

#----[End Wall Generation]------------------------------------------------------
#----[Set image locations]------------------------------------------------------
trollimg = pygame.image.load(path.join("images","Troll.bmp"))
playerimg = pygame.image.load(path.join("images", "Player.bmp"))
wallimg = pygame.image.load(path.join("images", "Wall.bmp"))
#----[End Images]---------------------------------------------------------------
#----[Create Entities]----------------------------------------------------------
player = Entity(playerimg)
troll1 = Troll(trollimg)
troll2 = Troll(trollimg)
troll3 = Troll(trollimg)
trolls = [troll1,troll2,troll3]
gate = Exit()
#----[End Create Entities]------------------------------------------------------
#----[Main Run Loop]------------------------------------------------------------
print("----[NEW RUN]----")

while True: #Game loop
    playerInput = False
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()
        #checks for any input from player, does it then allows trolls to move
        if pressed[upKey]: player.move("up"); playerInput = True
        elif pressed[leftKey]: player.move("left");  playerInput = True
        elif pressed[downKey]: player.move("down");  playerInput = True
        elif pressed[rightKey]: player.move("right");  playerInput = True

    if playerInput:
        for troll in trolls:
            directions = troll.getmoves()
            playerInDirection = troll.findPlayer()
            #troll will follow player if it can see it
            if playerInDirection is not None: troll.move(playerInDirection)
            #if directions is empty list then error is raised
            elif directions != []: troll.move(choice(directions))
        playerInput = False
    #draws changes to screen
    draw()
#----[End Program]--------------------------------------------------------------
