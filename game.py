from random import randint, choice
import pygame, sys

class Entity(pygame.sprite.Sprite):


    def __init__(self):
        #Any position in width/length, but a multiple of 30 to fit grid
        self.position = [choice(range(0,width,30)),choice(range(0,height,30))]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def move(self, direction):
        if direction == "up": self.position[1] -= tileSize[1]; player.rect.y = player.position[1]
        elif direction == "left": self.position[0] -= tileSize[0]; player.rect.x = player.position[0]
        elif direction == "down": self.position[1] += tileSize[1]; player.rect.x = player.position[1]
        elif direction == "right": self.position[0] += tileSize[0]; player.rect.x = player.position[0]

def draw():
    screen.fill((0,255,0))
    screen.blit(player.image,player.position)
    pygame.display.flip()


tileSize = (30,30)
size = width, height = 810, 600
screen = pygame.display.set_mode(size)
screen.fill((0,0,255))
pygame.display.flip()

player = Entity()

upKey = pygame.K_w
leftKey = pygame.K_a
downKey = pygame.K_s
rightKey = pygame.K_d

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
