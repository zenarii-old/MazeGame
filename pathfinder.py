import pygame
import collections
import time

class Queue():
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class SimpleGraph():
    def __init__(self, width, height, walls):
        self.nodes = []
        for x in range(0,width,32):
            for y in range(0,height,32):
                node = Node(x, y, walls)
                self.nodes.append(node)

    def update(self, walls):
        for node in self.nodes:
            for wall in walls:
                if node.rect.colliderect(wall): node.open = False; break
            else: node.open = True

    def search(self, start, end):
        for node in self.nodes:
            if node.position == start:
                node.search

    def visualise(self, screen):
        openSquare = pygame.Surface((16,16))
        openSquare.get_rect()
        openSquare.fill((10,255,20))
        closedSquare = pygame.Surface((16,16))
        closedSquare.get_rect()
        closedSquare.fill((255,10,10))

        for node in self.nodes:
            if node.open:
                screen.blit(openSquare, node.position)
            elif not node.open:
                screen.blit(closedSquare, node.position)



"""
        for node in self.nodes:
            for neighbor in node.neighbors:
                if node.open and neighbor.open:
                    pygame.draw.line(screen, (10,10,255), node.position, neighbor.position, 16)
"""
class Node():
    def __init__(self, x, y, walls):
        self.position = [x,y]

        self.image = pygame.Surface((32,32))
        self.rect = self.image.get_rect()

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.open = True
        for wall in walls:
            if self.rect.colliderect(wall): self.open = False; break

        self.neighbors = []

    def getNeighbors(self, allNodes):
        directions = [[0,32],[32,0],[0,-32],[-32,0]]
        for direction in directions:
            neighbor = [self.position[0] + direction[0],
                        self.position[1] + direction[1]]
            for node in allNodes:
                if neighbor == node.position:
                    self.neighbors.append(node)


    def search(self, start, end):
        pass

def search(start, end, nodes, screen, visualise):
    for node in nodes:
        if node.position == start: start = node; break
    for node in nodes:
        if node.position == end: end = node; break
    frontier = Queue()
    frontier.put(start)
    cameFrom = {}
    cameFrom[start] = None


    while not frontier.empty():
        current = frontier.get()

        eval("current.position")
        #print("curpos",current.position)
        #break
        if current.position == end.position:
            return reconstructPath(start, end, nodes, cameFrom, screen, visualise)


        for node in nodes:
            if node in current.neighbors:
                if node not in cameFrom and node.open:
                    frontier.put(node)
                    cameFrom[node] = current
                    if visualise:
                        pygame.draw.line(screen, (10,10,255), node.position,
                                         current.position, 16)
                        time.sleep(0.01)
                        pygame.display.flip()

def reconstructPath(start, end, nodes, cameFrom, screen, visualise):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = cameFrom[current]
        if visualise:
            pygame.draw.line(screen, (255, 255, 255),
                             path[-1].position, current.position, 16)
            time.sleep(0.02)
            pygame.display.flip()

    return path
