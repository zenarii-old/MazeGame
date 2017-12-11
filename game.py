from random import randint, choice
import pygame, sys
import mazeGenerator

#TODO maze generation - conver list to wall objects
class Entity(pygame.sprite.Sprite):
    def __init__(self, color):
        #Any position in width/length, but a multiple of 30 to fit grid

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.inWall = False
        self.positionNotSet = True
        #TODO FIX THIS --¬ It doesn't correctly break loop
        #                V
        while self.positionNotSet:
            self.position=[choice(range(0,width,16)),choice(range(0,height,16))]
            self.rect.x = self.position[0]
            self.rect.y = self.position[1]
            for wall in walls:
                if wall.rect.colliderect(self):break
            else:
                self.positionNotSet = False
            #should exit loop but doesn't


    def move(self, direction):
        #if collides with wall will move back
        if direction == "up":
            self.position[1] -= tileSize[1]; self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[1] += tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "left":
            self.position[0] -= tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[0] += tileSize[0]
                    self.rect.x = self.position[0]
                    break


        elif direction == "down":
            self.position[1] += tileSize[1]; self.rect.y = self.position[1]
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.position[1] -= tileSize[1]
                    self.rect.y = self.position[1]
                    break

        elif direction == "right":
            self.position[0] += tileSize[0]; self.rect.x = self.position[0]
            for wall in walls:
                if self.rect.colliderect(wall):
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

        directions = []
        if self.canMoveLeft: directions.append("left")
        if self.canMoveRight: directions.append("right")
        if self.canMoveUp: directions.append("up")
        if self.canMoveDown: directions.append("down")
        return directions

    def findPlayer(self):
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
    for troll in trolls: screen.blit(troll.image, troll.position)
    pygame.display.flip()

    movedWalls = []


tileSize = (16,16)
size = width, height = int(tileSize[0] * 27), int(tileSize[1] * 19)
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
#----[Wall Generation]----------------------------------------------------------
mazeString = mazeGenerator.generate(13,9)
walls = [] #holds all wall objects, immovable or unmovable
mazeList = []
mazeRow = []


for i in mazeString:
    if i == "\n": mazeList.append(mazeRow); mazeRow = []
    else: mazeRow.append(i)

for y in range(len(mazeList)):
    for x in range(len(mazeList[y])):
        if mazeList[y][x] == "+":
            wall = immovableWall(x*16,y*16)
            walls.append(wall)

#----[End Wall Generation]------------------------------------------------------
#----[Create Entities]----------------------------------------------------------
player = Entity(BLUE)
troll1 = Troll(RED)
troll2 = Troll(RED)
troll3 = Troll(RED)
trolls = [troll1,troll2,troll3]
#----[End Create Entities]------------------------------------------------------


print("----[NEW RUN]----")

while True: #Game loop
    playerInput = False
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            sys.exit()

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
            else: troll.move(choice(directions))
        playerInput = False

    draw()
