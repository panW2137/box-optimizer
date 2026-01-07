"""
Main program for box packing optimization using evolutionary algorithm.
Orchestrates the application flow: Configuration -> Optimization -> Visualization.
"""
import sys
import random
from PyQt6.QtWidgets import QApplication
from optimizer import run_optimization, evaluate
from visualizer import show_solution
from gui import ParameterWindow


def generate_boxes(count, minWidth, maxWidth, minHeight, maxHeight):
    """Generate a list of random boxes with specified size constraints."""
    return [(random.randint(minWidth, maxWidth), 
             random.randint(minHeight, maxHeight)) 
            for _ in range(count)]


if __name__ == "__main__":
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Show configuration dialog
    configDialog = ParameterWindow()
    
    if configDialog.exec():
        # Configuration accepted - get parameters
        params = configDialog.get_parameters()
        
        # Set random seed
        random.seed(params['seed'])
        
        # Generate boxes
        boxes = generate_boxes(params['boxCount'], 
                             params['minBoxWidth'], params['maxBoxWidth'], 
                             params['minBoxHeight'], params['maxBoxHeight'])
        
        # Console output
        print("\n" + "=" * 60)
        print("STARTING OPTIMIZATION")
        print("=" * 60)
        print(f"Random seed:        {params['seed']}")
        print(f"Grid size:          {params['gridWidth']} x {params['gridHeight']}")
        print(f"Box size range:     {params['minBoxWidth']}-{params['maxBoxWidth']} x {params['minBoxHeight']}-{params['maxBoxHeight']}")
        print(f"Box count:          {params['boxCount']}")
        print(f"Generations:        {params['generations']}")
        print(f"Population size:    {params['populationSize']}")
        print(f"Mutation rate:      {params['mutationRate']}")
        print("=" * 60)
        print()
        
        # Run optimization
        result = run_optimization(boxes, params['mask'], 
                                 params['gridWidth'], params['gridHeight'], 
                                 params['generations'], params['populationSize'], 
                                 params['mutationRate'])
        
        # Evaluate best and worst individuals
        bestScore, bestPlacement = evaluate(result['bestIndividual'], params['mask'], boxes, params['gridWidth'], params['gridHeight'])
        worstScore, _ = evaluate(result['worstIndividual'], params['mask'], boxes, params['gridWidth'], params['gridHeight'])
        
        # Display statistics in console
        print("=" * 60)
        print("OPTIMIZATION RESULTS")
        print("=" * 60)
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
        print("=" * 60)
        
        # Visualize best solution
        # Store window reference to prevent garbage collection
        window = show_solution(bestPlacement, params['mask'], params['gridWidth'], params['gridHeight'])
        
        # Start the event loop
        sys.exit(app.exec())
        
    else:
        # User cancelled configuration
        print("Optimization cancelled.")
        sys.exit(0)
