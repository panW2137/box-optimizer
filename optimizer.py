"""
Evolutionary algorithm for box packing optimization.
"""
import random
import time


def can_place(grid, x, y, w, h, mask):
    """Check if a box can be placed at position (x, y) with dimensions (w, h)."""
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
    """Place a box on the grid at position (x, y) with dimensions (w, h)."""
    for i in range(h):
        for j in range(w):
            grid[x + i][y + j] = boxId


def generate_individual(boxes):
    """Generate a random individual (solution) as a permutation with rotations."""
    indices = list(range(len(boxes)))
    random.shuffle(indices)
    return [(i, random.choice([True, False])) for i in indices]


def crossover(parent1, parent2):
    """Perform crossover between two parents to create two children."""
    cut = random.randint(1, len(parent1) - 1)
    child1 = parent1[:cut] + [gene for gene in parent2 if gene[0] not in [g[0] for g in parent1[:cut]]]
    child2 = parent2[:cut] + [gene for gene in parent1 if gene[0] not in [g[0] for g in parent2[:cut]]]
    return child1, child2


def mutate(individual):
    """Mutate an individual by swapping two boxes or flipping rotation."""
    ind = individual[:]
    if random.random() < 0.5:
        # Swap two boxes
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    else:
        # Flip rotation of a random box
        i = random.randint(0, len(ind) - 1)
        idx, rot = ind[i]
        ind[i] = (idx, not rot)
    return ind


def evaluate(individual, mask, boxes, width, height):
    """
    Evaluate an individual by attempting to place boxes according to the solution.
    Returns (number_of_placed_boxes, placement_list).
    """
    grid = [[0] * width for _ in range(height)]
    placed = []
    boxIdCounter = 1
    
    for idx, rotated in individual:
        w, h = boxes[idx]
        if rotated:
            w, h = h, w  # Rotate the box
        
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
    """
    Run the evolutionary optimization algorithm.
    
    Args:
        boxes: List of (width, height) tuples representing boxes to pack
        mask: 2D list indicating available positions (1 = available, 0 = blocked)
        width: Grid width
        height: Grid height
        generations: Number of generations to evolve
        populationSize: Size of the population
        mutationRate: Probability of mutation
    
    Returns:
        Dictionary with:
            - bestIndividual: Best solution found
            - worstIndividual: Worst solution from final generation
            - firstGenBestScore: Best score from first generation
            - firstGenWorstScore: Worst score from first generation
            - executionTime: Time taken in seconds
    """
    startTime = time.time()
    
    # Initialize population
    population = [generate_individual(boxes) for _ in range(populationSize)]
    
    # Evaluate initial population
    scores = [(evaluate(ind, mask, boxes, width, height)[0], ind) for ind in population]
    scores.sort(reverse=True)  # Best first
    
    # Track first generation results
    firstGenBestScore = scores[0][0]
    firstGenWorstScore = scores[-1][0]
    
    bestScore = 0
    worstScore = len(boxes)
    bestIndividual = None
    
    # Evolution loop
    for _ in range(generations):
        scores = [(evaluate(ind, mask, boxes, width, height)[0], ind) for ind in population]
        scores.sort(reverse=True)  # Best first
        
        # Track best and worst
        if scores[0][0] > bestScore:
            bestScore = scores[0][0]
            bestIndividual = scores[0][1]
        
        if scores[populationSize - 1][0] < worstScore:
            worstScore = scores[populationSize - 1][0]
        
        # Create new generation
        newPopulation = []
        while len(newPopulation) < populationSize:
            # Select parents from top 10
            parent1 = random.choice(scores[:10])[1]
            parent2 = random.choice(scores[:10])[1]
            child1, child2 = crossover(parent1, parent2)
            
            # Apply mutation
            if random.random() < mutationRate:
                child1 = mutate(child1)
            if random.random() < mutationRate:
                child2 = mutate(child2)
            
            newPopulation.extend([child1, child2])
        
        population = newPopulation[:populationSize]
    
    endTime = time.time()
    
    # Get worst individual from final generation
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
