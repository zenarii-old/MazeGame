from random import randint, choice
import pygame, sys
import mazeGenerator
import animations
from os import path


class Entity(pygame.sprite.Sprite):
    def __init__(self, spriteImage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.rect = self.image.get_rect()
        self.image = spriteImage
        #sets transparency to black
        self.image.set_colorkey((0,0,0))

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

class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, img):
        Entity.__init__(self, img)
        pygame.sprite.Sprite.__init__(self)

    def checkDead(self):
        for troll in trolls:
            if troll.rect.colliderect(self):
                dead = True
                print("You dead")

class Troll(Entity, pygame.sprite.Sprite):
    def __init__(self, img):
        Entity.__init__(self, img)
        pygame.sprite.Sprite.__init__(self)
        self.eaten = False

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

    def findPlayerOrCorpse(self):
        """Checks in each direction for 5 blocks, if player is found
        then moves in that direction, if hits wall stops searching.

        Returns None if player isn't found"""
        #in left direction
        wallHit = False
        for i in range(1,6):
            self.rect.x -= tileSize[0]
            if self.rect.colliderect(player): return "left"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            #checks through the environment peices to see if they are a corpse
            for environmentPiece in environment:
                if environmentPiece.rect.colliderect(self):
                    if environmentPiece.isCorpse(): return "left"
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in right direction
        wallHit = False
        for i in range(1,6):
            self.rect.x += tileSize[0]
            if player.rect.colliderect(self): return "right"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for environmentPiece in environment:
                if environmentPiece.rect.colliderect(self):
                    if environmentPiece.isCorpse(): return "right"
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in up direction
        wallHit = False
        for i in range(1,6):
            self.rect.y -= tileSize[1]
            if player.rect.colliderect(self): return "up"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for environmentPiece in environment:
                if environmentPiece.rect.colliderect(self):
                    if environmentPiece.isCorpse(): return "up"
            if wallHit: break
        self.rect.y = self.position[1]

        #downwards
        for i in range(1,6):
            self.rect.y += tileSize[1]
            if player.rect.colliderect(self): return "down"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for environmentPiece in environment:
                if environmentPiece.rect.colliderect(self):
                    if environmentPiece.isCorpse(): return "down"
            if wallHit: break
        self.rect.y = self.position[1]

    def die(self):
        self.posInList = trolls.index(self)
        trolls.pop(self.posInList)
        trollCorpse = Corpse(self.position[0], self.position[1])
        environment.append(trollCorpse)

    def eat(self, corpse):
        corpse.getEaten()
        print("Troll is big")

    def upgrade(self):
        newTroll = SuperTroll(self.rect.x,self.rect.y)
        trolls.append(newTroll)
        self.die()

class SuperTroll(Troll, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.Surface(tileSize)
        self.rect = ([32,32],[32,32])
        self.position = [x, y]

        self.image = STrollimg
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        #sets transparency to black
        self.image.set_colorkey((0,0,0))

"""    def getmoves(self):
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

    def findPlayerOrCorpse(self):
        return None"""


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

    def canMove(): return False

class movableWall(Block, pygame.sprite.Sprite):
    def __init__(self,x,y):
        Block.__init__(self,x,y)
        pygame.sprite.Sprite.__init__(self)

    def canMove(): return False

    def push(self, direction):
        if direction == "up":
            self.rect.y -= 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.y += 32; break
                if gate.rect.colliderect(self):
                    self.rect.y += 32
            else: self.position[1] = self.rect.y

        elif direction == "left":
            self.rect.x -= 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.x += 32; break
                if gate.rect.colliderect(self):
                    self.rect.x += 32; break
            else: self.position[0] = self.rect.x

        elif direction == "down":
            self.rect.y += 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.y -= 32; break
                if gate.rect.colliderect(self):
                    self.rect.y -= 32; break
            else: self.position[1] = self.rect.y

        elif direction == "right":
            self.rect.x += 32
            for wall in walls:
                if wall.rect.colliderect(self) and wall is not self:
                    self.rect.x -= 32; break
                if gate.rect.colliderect(self):
                    self.rect.x -= 32; break
            else: self.position[0] = self.rect.x

        for troll in trolls:
            if troll.rect.colliderect(self):
                troll.die(); self.smash(); self.leaveRubble()

    def leaveRubble(self):
        rubble = Rubble(self.position)
        environment.append(rubble)

class Exit(Block, pygame.sprite.Sprite):
    def __init__(self):
        self.side = choice(["Top","Bottom"])#,"Bottom","Left","Right")
        self.rect = ([32,32],[32,32])
        if self.side == "Top":
            self.position = [0,0]
            #The 32 start prevents corner spawns, as does width-32
            self.position[0] = choice(range(32,width-32,32))
            self.position[1] = 0

        if self.side == "Bottom":
            self.position = [0,0]
            self.position[0] = choice(range(32,width-32,32))
            self.position[1] = height - 32


        Block.__init__(self, self.position[0], self.position[1])
        pygame.sprite.Sprite.__init__(self)

        self.image.fill((100,100,100))
        for wall in walls:
            if self.rect.colliderect(wall): wall.smash()

class Rubble(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(tileSize)
        self.rect = self.image.get_rect()

        self.image = rubbleimg
        self.image.set_colorkey((0,0,0))
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.position = position
    def isCorpse(self): return False

class Corpse(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.Surface(tileSize)
        self.rect = self.image.get_rect()

        self.image = corpseimg
        self.image.set_colorkey((0,0,0))
        self.rect.x = xpos
        self.rect.y = ypos
        self.position = xpos, ypos

    #Deletes from environment list when troll eaten
    def getEaten(self):
        self.posInList = environment.index(self)
        environment.pop()

    def isCorpse(self): return True

#----[Draw To Screen Function]--------------------------------------------------
def draw():
    screen.fill((0,0,0))

    for wall in walls: screen.blit(wallimg, wall.position)

    for environmentPiece in environment: screen.blit(environmentPiece.image,
                                                     environmentPiece.position)
    for troll in trolls: screen.blit(troll.image, troll.position)
    screen.blit(player.image,player.position)

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
environment = []

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
rubbleimg = pygame.image.load(path.join("images", "Rubble.bmp"))
corpseimg = pygame.image.load(path.join("images", "Corpse.bmp"))
STrollimg = pygame.image.load(path.join("images", "STroll.bmp"))
#----[End Images]---------------------------------------------------------------

#----[Create Entities]----------------------------------------------------------
player = Player(playerimg)
dead = False

troll1 = Troll(trollimg)
troll1.position = [32,32]
troll1.rect.x = troll1.position[0]
troll1.rect.y = troll1.position[1]

troll2 = Troll(trollimg)
troll2.position = [32,32]
troll2.rect.x = troll2.position[0]
troll2.rect.y = troll2.position[1]

troll3 = Troll(trollimg)
trolls = [troll1,troll2,troll3]

gate = Exit()
#----[End Create Entities]------------------------------------------------------
#----[Main Run Loop]------------------------------------------------------------
print("----[NEW RUN]----")

while True: #Game loop
    playerInput = False
    #Gets player input
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()
        #checks for any input from player, does it then allows trolls to move
        if pressed[upKey]: player.move("up"); playerInput = True
        elif pressed[leftKey]: player.move("left");  playerInput = True
        elif pressed[downKey]: player.move("down");  playerInput = True
        elif pressed[rightKey]: player.move("right");  playerInput = True
    #moves trolls
    if playerInput:
        for troll in trolls:
            directions = troll.getmoves()
            playerInDirection = troll.findPlayerOrCorpse()
            #troll will follow player if it can see it
            for environmentPiece in environment:
                if troll.rect.colliderect(environmentPiece) and environmentPiece.isCorpse():
                    troll.eat(environmentPiece)
                    troll.eaten = True
            if playerInDirection is not None:
                troll.move(playerInDirection)
            #if directions is empty list then error is raised
            elif directions != []: troll.move(choice(directions))
            if troll.eaten:
                troll.upgrade()

    #----[Death based stuff]----------------------------------------------------
    if not dead and playerInput:
        player.checkDead()
    if dead:
        animations.GAMEOVER()
        sys.exit()
    playerInput = False
    #draws changes to screen
    draw()
#----[End Program]--------------------------------------------------------------
