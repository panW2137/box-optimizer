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
        print("START OPTIMALIZACJI")
        print("============================================================")
        print(f"Seed: {params['seed']}")
        print(f"Rozmiar siatki: {params['gridWidth']} x {params['gridHeight']}")
        print(f"Ograniczenia rozmiaru pudełek: {params['minBoxWidth']}-{params['maxBoxWidth']} x {params['minBoxHeight']}-{params['maxBoxHeight']}")
        print(f"Liczba pudełek: {params['boxCount']}")
        print(f"Pokolenia: {params['generations']}")
        print(f"Rozmiar populacji: {params['populationSize']}")
        print(f"Współczynnik mutacji: {params['mutationRate']}")
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
        print(f"Pierwsza generacja:")
        print(f"  Najlepszy wynik:     {result['firstGenBestScore']} pudełek")
        print(f"  Najgorszy wynik:    {result['firstGenWorstScore']} pudełek")
        print()
        print(f"Końcowa generacja:")
        print(f"  Najlepszy wynik:     {bestScore} pudełek")
        print(f"  Najgorszy wynik:    {worstScore} pudełek")
        print()
        print(f"Poprawa:")
        print(f"  Najlepszy:           +{bestScore - result['firstGenBestScore']} pudełek")
        print(f"  Najgorszy:          +{worstScore - result['firstGenWorstScore']} pudełek")
        print()
        print(f"Execution time:   {result['executionTime']:.3f} seconds")
        print("============================================================")
        
        #odpal wizualajzer
        window = show_solution(bestPlacement, params['mask'], params['gridWidth'], params['gridHeight'])
        #****** garbage collector
        
        #oczekuj na zamkniecie
        sys.exit(app.exec())
        
    else: #wcisneli X
        print("Optymalizacja przerwana.")
        sys.exit(0)
