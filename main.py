import configparser


def getConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    arrayStones = config['STONES']['coords'].replace('[', '').replace(']', '').split(' ')
    for i in range(0, len(arrayStones)):
        arrayStones[i] = arrayStones[i].replace('(', '').replace(')', '').split(',')
        arrayStones[i][0] = int(arrayStones[i][0])
        arrayStones[i][1] = int(arrayStones[i][1])
    rows = config['SIZE']['rows']
    cols = config['SIZE']['cols']
    return int(rows), int(cols), arrayStones


def buildMap():
    rows, cols, stones = getConfig()
    myMap = [[0 for i in range(cols)] for j in range(rows)]
    for stone in stones:
        myMap[stone[0]][stone[1]] = -1
    return cols, rows, len(stones), myMap


# GLOBALS
width, height, stoneNumber, garden = buildMap()
maxGenes = width + height + stoneNumber


class Individual:
    def __init__(self, genes):
        self.startingPoints = genes[2:]
        # left or right = 0 is left preferred, 1 is right preferred
        self.leftOrRight = genes[0]
        self.verticalOrHorizontal = genes[1]
        self.garden = garden
        self.numberOfMoves = 1
        self.rakeGarden()
        self.fitness = self.getFitness()


    def getFitness(self):
        fitness = 0
        for row in self.garden:
            for field in row:
                if field > 0:
                    fitness += 1
        return fitness


    def getStartingDirection(self, row, col):
        if row == 0:
            return 'down'
        if col == 0:
            return 'right'
        if row == height - 1:
            return 'up'
        if col == width - 1:
            return 'left'

    def rakeGarden(self):
        for point in self.startingPoints:
            if self.isSafe(point[0], point[1]) == 1:
                result = self.makeLine(point[0], point[1], self.getStartingDirection(point[0], point[1]))
                if result == 'lineDone':
                    self.numberOfMoves += 1
                    continue
                if result == 'gameOver':
                    return

    def makeLine(self, row, col, direction):
        if direction == 'lineDone':
            return 'lineDone'
        if direction == 'gameOver':
            return 'gameOver'
        self.garden[row][col] = self.numberOfMoves
        nextDirection = self.getDirection(row, col, direction)
        if nextDirection == 'up':
            return self.makeLine(row - 1, col, 'up')
        if nextDirection == 'down':
            return self.makeLine(row + 1, col, 'down')

        if nextDirection == 'right' and direction == 'up':
            return self.makeLine(row, col + 1, 'right')
        if nextDirection == 'left' and direction == 'down':
            return self.makeLine(row, col + 1, 'left')

        if nextDirection == 'right' and direction == 'down':
            return self.makeLine(row, col - 1, 'right')
        if nextDirection == 'left' and direction == 'up':
            return self.makeLine(row, col - 1, 'left')

        if nextDirection == 'right' and direction == 'right':
            return self.makeLine(row, col + 1, 'right')
        if nextDirection == 'left' and direction == 'left':
            return self.makeLine(row, col - 1, 'left')

        return self.makeLine(row, col, nextDirection)

    def isSafe(self, row, col):
        if (not (row < height and col < width)) or (row < 0 or col < 0):
            # out of garden, finished a line
            return 0
        if self.garden[row][col] == 0:
            # safe spot, a mark can be made
            return 1
        # not a safe spot, either a stone or already done spot
        return 2

    def getDirection(self, row, col, prevDirection):
        if prevDirection == 'up':
            if self.isSafe(row - 1, col) == 1:
                return 'up'
            if self.isSafe(row - 1, col) == 0:
                return 'lineDone'
            if self.leftOrRight == 0:
                if self.isSafe(row, col - 1) == 1:
                    return 'left'
                elif self.isSafe(row, col + 1) == 1:
                    return 'right'
                if self.isSafe(row,
                               col - 1) == 0:  # ak je na kraji a ma sa otocit mimo mapy, najprv skusi smer ktory mu nie je prvorady
                    return 'lineDone'
                elif self.isSafe(row, col + 1) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'
            if self.leftOrRight == 1:
                if self.isSafe(row, col + 1) == 1:
                    return 'right'
                elif self.isSafe(row, col - 1) == 1:
                    return 'left'
                if self.isSafe(row,
                               col + 1) == 0:  # ak je na kraji a ma sa otocit mimo mapy, najprv skusi smer ktory mu nie je prvorady
                    return 'lineDone'
                elif self.isSafe(row, col - 1) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'

        if prevDirection == 'down':
            if self.isSafe(row + 1, col) == 1:
                return 'down'
            if self.isSafe(row + 1, col) == 0:
                return 'lineDone'
            if self.leftOrRight == 0:
                if self.isSafe(row, col + 1) == 1:
                    return 'left'
                elif self.isSafe(row, col - 1) == 1:
                    return 'right'
                if self.isSafe(row, col + 1) == 0:
                    return 'lineDone'
                elif self.isSafe(row, col - 1) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'
            if self.leftOrRight == 1:
                if self.isSafe(row, col - 1) == 1:
                    return 'right'
                elif self.isSafe(row, col + 1) == 1:
                    return 'left'
                if self.isSafe(row, col - 1) == 0:
                    return 'lineDone'
                elif self.isSafe(row, col + 1) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'

        if prevDirection == 'right':
            if self.isSafe(row, col + 1) == 1:
                return 'right'
            if self.isSafe(row, col + 1) == 0:
                return 'lineDone'
            if self.leftOrRight == 0:
                if self.isSafe(row - 1, col) == 1:
                    return 'up'
                elif self.isSafe(row + 1, col) == 1:
                    return 'down'
                elif self.isSafe(row - 1, col) == 0:
                    return 'lineDone'
                elif self.isSafe(row + 1, col) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'
            if self.leftOrRight == 1:
                if self.isSafe(row + 1, col) == 1:
                    return 'down'
                elif self.isSafe(row - 1, col) == 1:
                    return 'up'
                elif self.isSafe(row + 1, col) == 0:
                    return 'lineDone'
                elif self.isSafe(row - 1, col) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'

        if prevDirection == 'left':
            if self.isSafe(row, col - 1) == 1:
                return 'left'
            if self.isSafe(row, col - 1) == 0:
                return 'lineDone'
            if self.leftOrRight == 0:
                if self.isSafe(row + 1, col) == 1:
                    return 'left'
                elif self.isSafe(row - 1, col) == 1:
                    return 'right'
                elif self.isSafe(row + 1, col) == 0:
                    return 'lineDone'
                elif self.isSafe(row - 1, col) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'
            if self.leftOrRight == 1:
                if self.isSafe(row - 1, col) == 1:
                    return 'right'
                elif self.isSafe(row + 1, col) == 1:
                    return 'left'
                elif self.isSafe(row - 1, col) == 0:
                    return 'lineDone'
                elif self.isSafe(row + 1, col) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'


def buildMap():
    rows, cols, stones = getConfig()
    myMap = [[0 for i in range(cols)] for j in range(rows)]
    for stone in stones:
        myMap[stone[0]][stone[1]] = -1
    return myMap


if __name__ == '__main__':
    individual = Individual((1, 1, (1, 0), (0, 0), (0, 5), (4, 3), (0,0), (0,4)))
