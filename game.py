from random import randint, choice
import pygame, sys

class Entity(pygame.sprite.Sprite):


    def __init__(self):
        #Any position in width/length, but a multiple of 30 to fit grid
        self.position = choice(range(0,width,30)),choice(range(0,height,30))
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(tileSize)
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]



def draw():
    screen.blit(player.image,player.position)
    pygame.display.flip()


tileSize = (30,30)
size = width, height = 810, 600
screen = pygame.display.set_mode(size)
screen.fill((0,0,255))
pygame.display.flip()

player = Entity()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    draw()


"""
#map ="""########
#      #
#      #
#      #
#      #
########
"""

#width = 9
#height = 6
#size = ((width-1)*30,height*30)
#screen = pygame.display.set_mode(size)

player = Player()

map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)


map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)
map = map.replace("@"," ")

player.move("up")
map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)
map = map.replace("@"," ")

player.move("up")
map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)
map = map.replace("@"," ")

player.move("right")
map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)
map = map.replace("@"," ")

player.move("right")
map = map[0:player.position] + "@" + map[player.position+1:len(map)]
print(map)
map = map.replace("@"," ")
"""
