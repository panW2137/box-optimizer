import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


#edytor maski
class MaskEditorWindow(QDialog):    
    #inicjalziacja
    def __init__(self, gridWidth, gridHeight,):
        super().__init__()
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = 40
        
        #ustaw maske
        self.mask = [[1] * gridWidth for _ in range(gridHeight)]
        
        self.setWindowTitle("Edytor maski - Zaznacz obszary niedostępne")
        self.setup_ui()
    
    #ustaw ui
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        #instrukcje
        instructions = QLabel("Kliknij na komórkę, aby przełączyć jej stan:\n")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        #widget siatki
        self.gridWidget = MaskEditorGrid(self.mask, self.gridWidth, self.gridHeight, self.cellSize)
        layout.addWidget(self.gridWidget)
        
        #guziki
        buttonLayout = QHBoxLayout()
        
        clearButton = QPushButton("Wyczyść maskę")
        clearButton.clicked.connect(self.clear_mask)
        buttonLayout.addWidget(clearButton)
        
        doneButton = QPushButton("Gotowe")
        doneButton.clicked.connect(self.accept)
        buttonLayout.addWidget(doneButton)
        
        layout.addLayout(buttonLayout)
    
    #czyszczenie maski
    def clear_mask(self):
        self.mask = [[1] * self.gridWidth for _ in range(self.gridHeight)]
        self.gridWidget.mask = self.mask
        self.gridWidget.update()
    
    #zwracanie maski
    def get_mask(self):
        return self.mask


#widget siatki
class MaskEditorGrid(QWidget):    
    def __init__(self, mask, gridWidth, gridHeight, cellSize):
        super().__init__()
        self.mask = mask
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = cellSize
        
        self.setMinimumSize(
            gridWidth * cellSize + 1,
            gridHeight * cellSize + 1
        )
    
    def paintEvent(self, event):
        #inicjalizacja paintera
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        #rysowanie komorek
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                x = j * self.cellSize
                y = i * self.cellSize
                
                #kolor zalezny od stanu maski
                if self.mask[i][j] == 1:
                    if (i+j)%2 == 0:
                        color = QColor(144, 238, 144)
                    else:
                        color = QColor(144-20, 238-20, 144-20)
                else:
                    if (i+j)%2 == 0:
                        color = QColor(255, 99, 71) 
                    else:
                        color = QColor(255-20, 99-20, 71-20)
                
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(color)
                painter.drawRect(x, y, self.cellSize, self.cellSize)
        
    def mousePressEvent(self, event):
        x = event.pos().x() // self.cellSize
        y = event.pos().y() // self.cellSize
        
        #wykonac akcje tylko jezeli kliknieto na komorke
        if 0 <= x < self.gridWidth and 0 <= y < self.gridHeight:
            if self.mask[y][x] == 1:
                self.mask[y][x] = 0
            else:
                self.mask[y][x] = 1
            #self.mask[y][x] = 1 - self.mask[y][x]
            self.update()


class ParameterWindow(QDialog):    
    def __init__(self):
        super().__init__()
        
        #wartosci domyslne
        self.defaults = {
            'seed': 44,
            'gridWidth': 16,
            'gridHeight': 16,
            'minBoxWidth': 1,
            'maxBoxWidth': 5,
            'minBoxHeight': 1,
            'maxBoxHeight': 5,
            'generations': 10,
            'populationSize': 50,
            'mutationRate': 0.5,
            'boxCount': 150
        }
        
        #maska domyslnie wszystkie dostepne
        self.mask = [[1] * self.defaults['gridWidth'] for _ in range(self.defaults['gridHeight'])]
        
        self.setWindowTitle("Optymalizacja pakowania pudełek - Parametry")
        self.setup_ui()
    
    def setup_ui(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
        # tytuł
        title = QLabel("Optymalizacja pakowania pudełek - Ustawienia")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(title)
        
        #layout formularza
        formLayout = QFormLayout()
        
        #slownik na inputy
        self.inputs = {}
        
        #kazde pole inicjalizowane wartosciami domyslnymi
        self.inputs['seed'] = QLineEdit(str(self.defaults['seed']))
        formLayout.addRow("Random Seed:", self.inputs['seed'])
        
        formLayout.addRow(QLabel(""))  #przerwa
        formLayout.addRow(QLabel("Rozmiar siatki:"))
        self.inputs['gridWidth'] = QLineEdit(str(self.defaults['gridWidth']))
        formLayout.addRow("   Szerokość siatki:", self.inputs['gridWidth'])
        self.inputs['gridHeight'] = QLineEdit(str(self.defaults['gridHeight']))
        formLayout.addRow("   Wysokość siatki:", self.inputs['gridHeight'])
        
        #ograniczenia rozmiaru pudelek
        formLayout.addRow(QLabel(""))  #przerwa
        formLayout.addRow(QLabel("Ograniczenia rozmiaru pudełek:"))
        self.inputs['minBoxWidth'] = QLineEdit(str(self.defaults['minBoxWidth']))
        formLayout.addRow("  Min Szerokość siatki:", self.inputs['minBoxWidth'])
        self.inputs['maxBoxWidth'] = QLineEdit(str(self.defaults['maxBoxWidth']))
        formLayout.addRow("  Max Szerokość siatki:", self.inputs['maxBoxWidth'])
        self.inputs['minBoxHeight'] = QLineEdit(str(self.defaults['minBoxHeight']))
        formLayout.addRow("  Min Wysokość siatki:", self.inputs['minBoxHeight'])
        self.inputs['maxBoxHeight'] = QLineEdit(str(self.defaults['maxBoxHeight']))
        formLayout.addRow("  Max Wysokość siatki:", self.inputs['maxBoxHeight'])

        #parametry algorytmu
        formLayout.addRow(QLabel(""))  #przerwa
        formLayout.addRow(QLabel("Parametry algorytmu:"))
        self.inputs['generations'] = QLineEdit(str(self.defaults['generations']))
        formLayout.addRow("  Generations:", self.inputs['generations'])
        self.inputs['populationSize'] = QLineEdit(str(self.defaults['populationSize']))
        formLayout.addRow("  Population Size:", self.inputs['populationSize'])
        self.inputs['mutationRate'] = QLineEdit(str(self.defaults['mutationRate']))
        formLayout.addRow("  Mutation Rate:", self.inputs['mutationRate'])
        self.inputs['boxCount'] = QLineEdit(str(self.defaults['boxCount']))
        formLayout.addRow("  Box Count:", self.inputs['boxCount'])
        
        mainLayout.addLayout(formLayout)
        
        #przyciski
        buttonLayout = QHBoxLayout()
        
        maskButton = QPushButton("Konfiguruj maskę")
        maskButton.clicked.connect(self.open_mask_editor)
        buttonLayout.addWidget(maskButton)
        
        startButton = QPushButton("Rozpocznij optymalizację")
        startButton.clicked.connect(self.accept_input)
        startButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        buttonLayout.addWidget(startButton)
        
        mainLayout.addLayout(buttonLayout)
    
    #edytor maski
    def open_mask_editor(self):
            #pobierz rozmiar z formularza
            gridWidth = int(self.inputs['gridWidth'].text())
            gridHeight = int(self.inputs['gridHeight'].text())
            
            #odpalaj edytor
            editor = MaskEditorWindow(gridWidth, gridHeight)
            if editor.exec():
                self.mask = editor.get_mask()
    
    def accept_input(self):
        self.get_parameters()
        self.accept()
    
#funkcja pobiera wartosci
    def get_parameters(self):
        params = {}
        
        # pobieranie wartosci
        params['seed'] = int(self.inputs['seed'].text())
        params['gridWidth'] = int(self.inputs['gridWidth'].text())
        params['gridHeight'] = int(self.inputs['gridHeight'].text())
        params['minBoxWidth'] = int(self.inputs['minBoxWidth'].text())
        params['maxBoxWidth'] = int(self.inputs['maxBoxWidth'].text())
        params['minBoxHeight'] = int(self.inputs['minBoxHeight'].text())
        params['maxBoxHeight'] = int(self.inputs['maxBoxHeight'].text())
        params['generations'] = int(self.inputs['generations'].text())
        params['populationSize'] = int(self.inputs['populationSize'].text())
        params['mutationRate'] = float(self.inputs['mutationRate'].text())
        params['boxCount'] = int(self.inputs['boxCount'].text())
        params['mask'] = self.mask
        
        return params

