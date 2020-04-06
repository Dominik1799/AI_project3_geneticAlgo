import configparser
import random
import heapq


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
    size = config['POPULATION']['size']
    mutation = config['POPULATION']['mutationRate']
    generations = config['POPULATION']['maxGenerations']
    parents = config['POPULATION']['numberOfParents']
    selection = config['SELECTION']['type']
    return int(rows), int(cols), arrayStones, int(size), float(mutation), int(generations), int(parents), int(selection)


def buildMap():
    rows, cols, stones, size, mutation, generations, parents, selection = getConfig()
    myMap = [[0 for i in range(cols)] for j in range(rows)]
    for stone in stones:
        myMap[stone[0]][stone[1]] = -1
    return cols, rows, len(stones), myMap, size, mutation, generations, parents, selection


# GLOBALS
width, height, stoneNumber, garden, populationSize, mutationRate, maxGenerations, parentNum, selectionType = buildMap()
maxGenes = width + height + stoneNumber - 2


class Individual:
    def __init__(self, genes):
        self.startingPoints = genes[2]
        # left or right = 0 is left preferred, 1 is right preferred
        self.leftOrRight = genes[0]
        self.verticalOrHorizontal = genes[1]
        self.garden = [row[:] for row in garden]
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
        nextDirection = self.getDirection(row, col, direction)  # tu si zacal gay
        if nextDirection == 'up':
            return self.makeLine(row - 1, col, 'up')
        if nextDirection == 'down':
            return self.makeLine(row + 1, col, 'down')

        if nextDirection == 'right':
            return self.makeLine(row, col + 1, 'right')
        if nextDirection == 'left':
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
                if self.isSafe(row, col - 1) == 0:
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
                if self.isSafe(row, col + 1) == 0:
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
                if self.isSafe(row, col - 1) == 1:
                    return 'left'
                elif self.isSafe(row, col + 1) == 1:
                    return 'right'
                if self.isSafe(row, col - 1) == 0:
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
                if self.isSafe(row, col + 1) == 0:
                    return 'lineDone'
                elif self.isSafe(row, col - 1) == 0:
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
                    return 'down'
                elif self.isSafe(row - 1, col) == 1:
                    return 'up'
                elif self.isSafe(row + 1, col) == 0:
                    return 'lineDone'
                elif self.isSafe(row - 1, col) == 0:
                    return 'lineDone'
                else:
                    return 'gameOver'
            if self.leftOrRight == 1:
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

    def __lt__(self, other):
        return self.fitness > other.fitness


def getRandomGene():
    startSides = ['up', 'down', 'left', 'right']
    startSide = startSides[random.randrange(0, 4)]
    if startSide == 'up':
        return 0, random.randrange(0, width)
    if startSide == 'down':
        return height - 1, random.randrange(0, width)
    if startSide == 'right':
        return random.randrange(0, height), 0
    if startSide == 'left':
        return random.randrange(0, height), width - 1


def getRandomChromosone():
    leftOrRight = random.randrange(0, 2)
    horizontalOrVertical = random.randrange(0, 2)
    genes = []
    for i in range(0, maxGenes):
        genes.append(getRandomGene())
    return leftOrRight, horizontalOrVertical, genes


def createFirstGeneration():
    newPopulation = []
    for i in range(0, populationSize):
        newPopulation.append(Individual(getRandomChromosone()))
    return newPopulation


def rouletteWheelSelection(currentPopulation):
    sumOfFitnesses = 0
    marblePostition = 0
    parents = []
    for indiviual in currentPopulation:
        sumOfFitnesses += indiviual.fitness
    for i in range(0, parentNum):
        marble = random.randrange(0, sumOfFitnesses)
        for indiviual in currentPopulation:
            if marblePostition >= marble:
                parents.append(indiviual)
                break
            marblePostition += indiviual.fitness
    return parents


def elitismSelection(currentPopulation):
    heapq.heapify(currentPopulation)
    parents = []
    for i in range(0, parentNum):
        parents.append(heapq.heappop(currentPopulation))

    return parents


def crossOver(mama, papa):
    childStartingPoints = []
    if mama.fitness >= papa.fitness:
        leftOrRight = mama.leftOrRight
        verticalOrHorizontal = mama.verticalOrHorizontal
    else:
        leftOrRight = papa.leftOrRight
        verticalOrHorizontal = papa.verticalOrHorizontal
    for i in range(0, maxGenes):
        whoPassesGene = random.choices(population=['mama', 'papa'], weights=[mama.fitness, papa.fitness])[0]
        if whoPassesGene == 'mama':
            childStartingPoints.append(mama.startingPoints[i])
        else:
            childStartingPoints.append(papa.startingPoints[i])
        willGeneMutate = random.choices(population=[True, False], weights=[mutationRate, 1 - mutationRate])[0]
        if willGeneMutate:
            childStartingPoints[i] = getRandomGene()

    return leftOrRight, verticalOrHorizontal, childStartingPoints


def makeChildren(parents):
    children = []
    try:
        while True:
            children.append(Individual(crossOver(parents.pop(), parents.pop())))
    except IndexError:
        print()
    return children


def createPopulation(currentPopulation):
    # Roulette Wheel Selection
    newPopulation = []
    if selectionType == 0:
        parents = rouletteWheelSelection(currentPopulation)
        children = makeChildren(parents)
        for i in range(0, populationSize - len(children)):
            newPopulation.append(Individual(getRandomChromosone()))
        newPopulation += children
        return newPopulation


if __name__ == '__main__':
    # individual = Individual((0,0,[(4, 0), (6, 0), (9, 6), (1, 0), (0, 7), (9, 8), (0, 5), (9, 1), (0, 0), (9, 0), (4, 0), (0, 0), (9, 9), (7, 0), (0, 10), (4, 0), (3, 0), (5, 0), (4, 11), (1, 0), (9, 9), (0, 4), (9, 9), (1, 11), (1, 0), (3, 0)]))
    population = createFirstGeneration()
    for i in range(0, 10):
        makeChildren([])
