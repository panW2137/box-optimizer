"""
Main program for box packing optimization using evolutionary algorithm.
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from optimizer import run_optimization, evaluate


def generate_boxes(count, minWidth, maxWidth, minHeight, maxHeight):
    """Generate a list of random boxes with specified size constraints."""
    return [(random.randint(minWidth, maxWidth), 
             random.randint(minHeight, maxHeight)) 
            for _ in range(count)]


def visualize_solution(individual, boxes, mask, width, height):
    """Visualize the best solution using matplotlib."""
    # Evaluate to get placement
    _, placement = evaluate(individual, mask, boxes, width, height)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks(range(width + 1))
    ax.set_yticks(range(height + 1))
    ax.grid(True)
    ax.set_aspect('equal')
    
    # Draw masked areas
    for i in range(height):
        for j in range(width):
            if mask[i][j] == 0:
                rect = patches.Rectangle((j, height - i - 1), 1, 1, facecolor='lightgray')
                ax.add_patch(rect)
    
    # Draw placed boxes
    for boxId, idx, (x, y), (w, h) in placement:
        color = [random.random() for _ in range(3)]
        rect = patches.Rectangle((x, height - y - h), w, h, 
                                 linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(x + w / 2, height - y - h / 2, f"{boxId}", 
               ha='center', va='center', fontsize=10, color='black')
    
    plt.title("Box Placement - Evolutionary Algorithm")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(44)
    
    # Grid configuration
    gridWidth = 16
    gridHeight = 16
    
    # Box size constraints
    minBoxWidth = 1
    maxBoxWidth = 5
    minBoxHeight = 1
    maxBoxHeight = 5
    
    # Algorithm parameters
    generations = 10
    populationSize = 50
    mutationRate = 0.5
    boxCount = 150
    
    # Create mask (1 = available, 0 = blocked)
    mask = [[1] * gridWidth for _ in range(gridHeight)]
    
    # Optional: Block some areas
    # for i in range(7):
    #     for j in range(8, gridWidth):
    #         mask[i][j] = 0
    
    # Generate boxes
    boxes = generate_boxes(boxCount, minBoxWidth, maxBoxWidth, 
                          minBoxHeight, maxBoxHeight)
    
    print(f"Running optimization with {boxCount} boxes...")
    print(f"Parameters: {generations} generations, population size {populationSize}, mutation rate {mutationRate}")
    print()
    
    # Run optimization
    result = run_optimization(boxes, mask, gridWidth, gridHeight, 
                             generations, populationSize, mutationRate)
    
    # Evaluate best and worst individuals
    bestScore, bestPlacement = evaluate(result['bestIndividual'], mask, boxes, gridWidth, gridHeight)
    worstScore, _ = evaluate(result['worstIndividual'], mask, boxes, gridWidth, gridHeight)
    
    # Display statistics
    print("=" * 50)
    print("OPTIMIZATION RESULTS")
    print("=" * 50)
    print(f"First generation:")
    print(f"  Best score:     {result['firstGenBestScore']} boxes placed")
    print(f"  Worst score:    {result['firstGenWorstScore']} boxes placed")
    print()
    print(f"Final generation:")
    print(f"  Best score:     {bestScore} boxes placed")
    print(f"  Worst score:    {worstScore} boxes placed")
    print()
    print(f"Improvement:")
    print(f"  Best:           +{bestScore - result['firstGenBestScore']} boxes")
    print(f"  Worst:          +{worstScore - result['firstGenWorstScore']} boxes")
    print()
    print(f"Execution time:   {result['executionTime']:.3f} seconds")
    print("=" * 50)
    
    # Visualize best solution
    visualize_solution(result['bestIndividual'], boxes, mask, gridWidth, gridHeight)
