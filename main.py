import sys
import random
from PyQt6.QtWidgets import QApplication
from optimizer import run_optimization, evaluate
from visualizer import show_solution
from gui import ParameterWindow


def generate_boxes(count, minWidth, maxWidth, minHeight, maxHeight):
    return [(random.randint(minWidth, maxWidth), random.randint(minHeight, maxHeight)) for _ in range(count)]


if __name__ == "__main__":
    #inicjalizuj aplikacje
    app = QApplication(sys.argv)
    
    #inicjalizacja okna
    configDialog = ParameterWindow()
    
    #odpal okno
    #idz dalej, jak uzytkownik kliknie przycisk
    if configDialog.exec():
        #pobieranie konfiguracji
        params = configDialog.get_parameters()
        random.seed(params['seed'])
        
        #generowanie pudelek
        boxes = generate_boxes(params['boxCount'], params['minBoxWidth'], params['maxBoxWidth'], params['minBoxHeight'], params['maxBoxHeight'])
        
        #informacje w konsoli
        print("\n" + "============================================================")
        print("STARTING OPTIMIZATION")
        print("============================================================")
        print(f"Random seed:        {params['seed']}")
        print(f"Grid size:          {params['gridWidth']} x {params['gridHeight']}")
        print(f"Box size range:     {params['minBoxWidth']}-{params['maxBoxWidth']} x {params['minBoxHeight']}-{params['maxBoxHeight']}")
        print(f"Box count:          {params['boxCount']}")
        print(f"Generations:        {params['generations']}")
        print(f"Population size:    {params['populationSize']}")
        print(f"Mutation rate:      {params['mutationRate']}")
        print("============================================================")
        print()
        
        #odpalaj optymalizacje Start the event loop
        result = run_optimization(boxes, params['mask'], params['gridWidth'], params['gridHeight'], params['generations'], params['populationSize'], params['mutationRate'])
        
        #oblicz najlepszego i najgorszego
        bestScore, bestPlacement = evaluate(result['bestIndividual'], params['mask'], boxes, params['gridWidth'], params['gridHeight'])
        worstScore, _ = evaluate(result['worstIndividual'], params['mask'], boxes, params['gridWidth'], params['gridHeight'])
        
        #wyswietl wyniki w konsoli
        print("============================================================")
        print("OPTIMIZATION RESULTS")
        print("============================================================")
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
        print("============================================================")
        
        #odpal wizualajzer
        window = show_solution(bestPlacement, params['mask'], params['gridWidth'], params['gridHeight'])
        #jebany garbage collector
        
        #oczekuj na zamkniecie
        sys.exit(app.exec())
        
    else: #wcisneli X
        print("Optimization cancelled.")
        sys.exit(0)
