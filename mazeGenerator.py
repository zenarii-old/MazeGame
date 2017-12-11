from random import shuffle, randrange

#maze generator test
def generate(width, height):
    vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
    ver = [["+ "] * width + ['+'] for _ in range(height)] + [[]]
    hor = [["++"] * width + ['+'] for _ in range(height + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+ "
            if yy == y: ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(width), randrange(height))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s
