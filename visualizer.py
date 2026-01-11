"""
PyQt6-based visualization for box packing solutions.
"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QFont

#widget na którym można rysować
class GridWidget(QWidget):
    
    def __init__(self, placement, mask, gridWidth, gridHeight, cellSize=40):
        super().__init__()
        self.placement = placement
        self.mask = mask
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = cellSize
        
        #generuj losowe kolory dla kazdego pudelka co sie udalo postawic
        self.boxColors = {}
        for boxId, _, _, _ in placement:
            self.boxColors[boxId] = QColor(
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
        
        #rozmiar widgetu
        self.setMinimumSize(
            gridWidth * cellSize + 1,
            gridHeight * cellSize + 1
        )
    

    def paintEvent(self, event):
        #painter rysuje sam na sobie
        painter = QPainter(self)
        
        #rysowanie maski na bialo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                if self.mask[i][j] == 0:
                    x = j * self.cellSize
                    y = i * self.cellSize
                    painter.drawRect(x, y, self.cellSize, self.cellSize)
        
        #rysuj pudelka
        for boxId, idx, (x, y), (w, h) in self.placement:

            painter.setBrush(self.boxColors[boxId])
            
            rectX = x * self.cellSize
            rectY = y * self.cellSize
            rectW = w * self.cellSize
            rectH = h * self.cellSize
            
            painter.drawRect(rectX, rectY, rectW, rectH)
            
            #rysuj numery pudelek
            painter.setPen(Qt.GlobalColor.black)
            painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            painter.drawText(
                QRect(rectX, rectY, rectW, rectH),
                Qt.AlignmentFlag.AlignCenter,
                str(boxId)
            )

def show_solution(placement, mask, gridWidth, gridHeight):
    #tworzenie instancji aplikacji
    app = QApplication.instance()
    
    #tworzenie okna
    window = QMainWindow()
    window.setWindowTitle("Box Placement")
    
    #ustawienie widgetu na ten z gory
    widget = GridWidget(placement, mask, gridWidth, gridHeight)
    window.setCentralWidget(widget)
    
    #pokazanie okna
    window.show()
    return window
