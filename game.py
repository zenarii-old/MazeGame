from random import randint, choice
import pygame, sys, time
import mazeGenerator
from os import path

class Entity(pygame.sprite.Sprite):
    def __init__(self, spriteImage):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Player"
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
                if self.rect.colliderect(wall) and self.name == "Player":
                    wall.push("up")
                    self.position[1] += tileSize[1]
                    self.rect.y = self.position[1]
                    break
                elif self.rect.colliderect(wall) and self.name == "Super Troll":
                    wall.smash(); wall.leaveRubble() #Troll smashes wall and moves
                    break

        elif direction == "left":
            self.position[0] -= tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall) and self.name == "Player":
                    wall.push("left")
                    self.position[0] += tileSize[0]
                    self.rect.x = self.position[0]
                    break
                elif self.rect.colliderect(wall) and self.name == "Super Troll":
                    wall.smash(); wall.leaveRubble()
                    break

        elif direction == "down":
            self.position[1] += tileSize[1]; self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall) and self.name == "Player":
                    wall.push("down")
                    self.position[1] -= tileSize[1]
                    self.rect.y = self.position[1]
                    break
                elif self.rect.colliderect(wall) and self.name == "Super Troll":
                    wall.smash(); wall.leaveRubble()
                    break

        elif direction == "right":
            self.position[0] += tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall) and self.name == "Player":
                    wall.push("right")
                    self.position[0] -= tileSize[0]
                    self.rect.x = self.position[0]
                    break
                elif self.rect.colliderect(wall) and self.name == "Super Troll":
                    wall.smash(); wall.leaveRubble()
                    break

class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, img):
        Entity.__init__(self, img)
        pygame.sprite.Sprite.__init__(self)
        self.dead = False

    def checkDead(self):
        for troll in trolls:
            if troll.rect.colliderect(self):
                self.dead = True

class Troll(Entity, pygame.sprite.Sprite):
    def __init__(self, img):
        Entity.__init__(self, img)
        pygame.sprite.Sprite.__init__(self)
        self.eaten = False
        self.name = "Troll"

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
            if self.rect.colliderect(player):
                self.rect.x = self.position[0]; return "left"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            #checks through the environment peices to see if they are a corpse
            for corpse in corpses:
                if corpse.rect.colliderect(self):
                    if corpse.isCorpse():
                        self.rect.x = self.position[0]; return "left"
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in right direction
        wallHit = False
        for i in range(1,6):
            self.rect.x += tileSize[0]
            if player.rect.colliderect(self):
                self.rect.x = self.position[0]; return "right"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for corpse in corpses:
                if corpse.rect.colliderect(self):
                    if corpse.isCorpse():
                        self.rect.x = self.position[0]; return "right"
            if wallHit: break #won't keep following through walls
        self.rect.x = self.position[0]

        #in up direction
        wallHit = False
        for i in range(1,6):
            self.rect.y -= tileSize[1]
            if player.rect.colliderect(self):
                self.rect.y = self.position[1]; return "up"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for corpse in corpses:
                if corpse.rect.colliderect(self):
                    if corpse.isCorpse():
                        self.rect.y = self.position[1]; return "up"
            if wallHit: break
        self.rect.y = self.position[1]

        #downwards
        wallHit = False
        for i in range(1,6):
            self.rect.y += tileSize[1]
            if player.rect.colliderect(self):
                self.rect.y = self.position[1]; return "down"
            for wall in walls:
                if wall.rect.colliderect(self): wallHit = True
            for corpse in corpses:
                if corpse.rect.colliderect(self):
                    if corpse.isCorpse():
                        self.rect.y = self.position[1]; return "down"
            if wallHit: break
        self.rect.y = self.position[1]

    def die(self):
            self.posInList = trolls.index(self)
            trolls.pop(self.posInList)
            trollCorpse = Corpse(self.position[0], self.position[1])
            corpses.append(trollCorpse)


    def eat(self, corpse):
        self.upgrade()
        corpse.getEaten()

    def upgrade(self):
        self.positionInList = trolls.index(self)
        trolls[self.positionInList] = SuperTroll(self.rect.x, self.rect.y)


class SuperTroll(Troll, pygame.sprite.Sprite):
    def __init__(self, x, y):

        self.name = "Super Troll"
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(tileSize)
        self.rect = self.image.get_rect()

        self.position = [x, y]

        self.image = STrollimg
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        #sets transparency to black
        self.image.set_colorkey((0,0,0))


    def findPlayerOrCorpse(self):
        """Checks in each direction for 5 blocks, if player is found
        then moves in that direction, if hits wall stops searching.

        Returns None if player isn't found"""
        #in left direction
        for i in range(1,6):
            self.rect.x -= tileSize[0]
            if self.rect.colliderect(player):
                self.rect.x = self.position[0]; return "left"
            #checks through the environment peices to see if they are a corpse
        self.rect.x = self.position[0]

        #in right direction
        wallHit = False
        for i in range(1,6):
            self.rect.x += tileSize[0]
            if player.rect.colliderect(self):
                self.rect.x = self.position[0]; return "right"
        self.rect.x = self.position[0]

        #in up direction
        wallHit = False
        for i in range(1,6):
            self.rect.y -= tileSize[1]
            if player.rect.colliderect(self):
                self.rect.y = self.position[1]; return "up"
        self.rect.y = self.position[1]

        #downwards
        for i in range(1,6):
            self.rect.y += tileSize[1]
            if player.rect.colliderect(self):
                self.rect.y = self.position[1]; return "down"
        self.rect.y = self.position[1]



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
                troll.die(); self.smash(); self.leaveRubble();

    def leaveRubble(self):
        rubble = Rubble(self.position)
        debris.append(rubble)

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

        debris.append(self)


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

        corpses.append(self)

    #Deletes from environment list when troll eaten
    def getEaten(self):
        self.posInList = corpses.index(self)
        corpses.pop(self.posInList)

    def isCorpse(self): return True

#----[Draw To Screen Functions]-------------------------------------------------
def drawEndScreen(endScreen):
    screen.fill((0,0,0))
    screen.blit(endScreen, (0,0))
    pygame.display.flip()
    time.sleep(0.2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                sys.exit()

def drawGameLoop():
    screen.fill((0,0,0))

    for corpse in corpses: screen.blit(corpse.image,corpse.position)
    for rubble in debris: screen.blit(rubble.image, rubble.position)
    for troll in trolls: screen.blit(troll.image, troll.position)
    for wall in walls: screen.blit(wallimg, wall.position)

    screen.blit(player.image,player.position)
    screen.blit(gate.image, gate.position)

    pygame.display.flip()

def drawStartScreen(startScreen):
    screen.fill((0,0,0))
    screen.blit(startScreen, (0,0))
    onStartScreen = True
    pygame.display.flip()
    while onStartScreen:
        events = pygame.event.get()
        for event in events:
            pressed = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.QUIT:
                sys.exit()

    pygame.display.flip()
#----[End Draw To Screen Functions]---------------------------------------------
#As screen may not fit all tiles unexpected behaviour occurs at borders
#this shiould prevent that
def getLength(length):
    lengthRemainder = length % 32
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
startScreen = pygame.image.load(path.join("images","Title Screen.bmp"))
deathScreen = pygame.image.load(path.join("images", "GAMEOVER!.bmp"))
winScreen = pygame.image.load(path.join("images", "Win Screen.bmp"))
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

trolls = [Troll(trollimg) for i in range(5)]

gate = Exit()

debris = []
corpses = []

#----[End Create Entities]------------------------------------------------------
#----[Main Run Loop]------------------------------------------------------------
print("----[NEW RUN]----")

drawStartScreen(startScreen)

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
            for corpse in corpses:
                if troll.rect.colliderect(corpse):
                    troll.eat(corpse)
            if playerInDirection is not None:
                troll.move(playerInDirection)
            #if directions is empty list then error is raised
            elif directions !=[]: troll.move(choice(directions))


    #----[Death based stuff]----------------------------------------------------
    if not player.dead and playerInput:
        player.checkDead()
    if player.dead:
        drawEndScreen(deathScreen)
    if not player.dead:
        if player.rect.colliderect(gate): drawEndScreen(winScreen)
    playerInput = False
    #draws changes to screen
    drawGameLoop()
#----[End Program]--------------------------------------------------------------
