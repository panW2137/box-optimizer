import random
import time


def can_place(grid, x, y, w, h, mask):
    gridHeight = len(grid)
    gridWidth = len(grid[0])
    
    if x + h > gridHeight or y + w > gridWidth:
        return False
    
    for i in range(h):
        for j in range(w):
            if grid[x + i][y + j] != 0 or mask[x + i][y + j] == 0:
                return False
    
    return True


def place(grid, x, y, w, h, boxId):
    for i in range(h):
        for j in range(w):
            grid[x + i][y + j] = boxId


def generate_individual(boxes):
    indices = list(range(len(boxes))) # lista z indeksami pudelek
    random.shuffle(indices) # losowe przemieszanie
    return [(i, random.choice([True, False])) for i in indices] # losowany jest index wraz z rotacja


def crossover(parent1, parent2):
    cut = random.randint(1, len(parent1) - 1) # punkt podzialu
    child1 = parent1[:cut] + [gene for gene in parent2 if gene[0] not in [g[0] for g in parent1[:cut]]]
    child2 = parent2[:cut] + [gene for gene in parent1 if gene[0] not in [g[0] for g in parent2[:cut]]] 
    return child1, child2


def mutate(individual):
    ind = individual[:]
    if random.random() < 0.5:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    else:
        i = random.randint(0, len(ind) - 1)
        idx, rot = ind[i]
        ind[i] = (idx, not rot)
    return ind


def evaluate(individual, mask, boxes, width, height):
    grid = [[0] * width for _ in range(height)]
    placed = []
    boxIdCounter = 1
    
    for idx, rotated in individual:
        w, h = boxes[idx]
        if rotated:
            w, h = h, w
        
        placedFlag = False
        for i in range(height):
            for j in range(width):
                if can_place(grid, i, j, w, h, mask):
                    place(grid, i, j, w, h, boxIdCounter)
                    placed.append((boxIdCounter, idx, (j, i), (w, h)))
                    boxIdCounter += 1
                    placedFlag = True
                    break
            if placedFlag:
                break
    
    return len(placed), placed


def run_optimization(boxes, mask, width, height, generations, populationSize, mutationRate):
    startTime = time.time()
    
    population = [generate_individual(boxes) for _ in range(populationSize)]
    
    scores = [(evaluate(ind, mask, boxes, width, height)[0], ind) for ind in population]
    scores.sort(reverse=True)
    
    firstGenBestScore = scores[0][0]
    firstGenWorstScore = scores[-1][0]
    
    bestScore = 0
    worstScore = len(boxes)
    bestIndividual = None
    
    for _ in range(generations):
        scores = [(evaluate(ind, mask, boxes, width, height)[0], ind) for ind in population]
        scores.sort(reverse=True)
        
        if scores[0][0] > bestScore:
            bestScore = scores[0][0]
            bestIndividual = scores[0][1]
        
        if scores[-1][0] < worstScore:
            worstScore = scores[-1][0]
        
        newPopulation = []
        while len(newPopulation) < populationSize:
            parent1 = random.choice(scores[:10])[1] # bierzemy 10 najlepszych osobnikow i losujemy
            parent2 = random.choice(scores[:10])[1]
            child1, child2 = crossover(parent1, parent2)
            
            if random.random() < mutationRate:
                child1 = mutate(child1)
            if random.random() < mutationRate:
                child2 = mutate(child2)
            
            newPopulation.extend([child1, child2])
        
        population = newPopulation[:populationSize]
    
    endTime = time.time()
    
    finalScores = [(evaluate(ind, mask, boxes, width, height)[0], ind) for ind in population]
    finalScores.sort(reverse=True)
    worstIndividual = finalScores[-1][1]
    
    return {
        'bestIndividual': bestIndividual,
        'worstIndividual': worstIndividual,
        'firstGenBestScore': firstGenBestScore,
        'firstGenWorstScore': firstGenWorstScore,
        'executionTime': endTime - startTime
    }
