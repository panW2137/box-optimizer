"""
PyQt6-based visualization for box packing solutions.
"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class GridWidget(QWidget):
    """Custom widget for drawing the grid and placed boxes."""
    
    def __init__(self, placement, mask, gridWidth, gridHeight, cellSize=40):
        super().__init__()
        self.placement = placement
        self.mask = mask
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = cellSize
        
        # Generate random colors for each box
        self.boxColors = {}
        for boxId, _, _, _ in placement:
            self.boxColors[boxId] = QColor(
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
        
        # Set widget size
        self.setMinimumSize(
            gridWidth * cellSize + 1,
            gridHeight * cellSize + 1
        )
    
    def paintEvent(self, event):
        """Draw the grid, masked areas, and boxes."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw masked areas (white background)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                if self.mask[i][j] == 0:
                    x = j * self.cellSize
                    y = i * self.cellSize
                    painter.drawRect(x, y, self.cellSize, self.cellSize)
        
        # Draw boxes
        for boxId, idx, (x, y), (w, h) in self.placement:
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.setBrush(self.boxColors[boxId])
            
            rectX = x * self.cellSize
            rectY = y * self.cellSize
            rectW = w * self.cellSize
            rectH = h * self.cellSize
            
            painter.drawRect(rectX, rectY, rectW, rectH)
            
            # Draw box number
            painter.setPen(Qt.GlobalColor.black)
            painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            painter.drawText(
                QRect(rectX, rectY, rectW, rectH),
                Qt.AlignmentFlag.AlignCenter,
                str(boxId)
            )
        
        # Draw grid lines
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        for i in range(self.gridHeight + 1):
            y = i * self.cellSize
            painter.drawLine(0, y, self.gridWidth * self.cellSize, y)
        
        for j in range(self.gridWidth + 1):
            x = j * self.cellSize
            painter.drawLine(x, 0, x, self.gridHeight * self.cellSize)


def show_solution(placement, mask, gridWidth, gridHeight):
    """
    Display the box packing solution in a PyQt window.
    
    Args:
        placement: List of (boxId, idx, (x, y), (w, h)) tuples
        mask: 2D list indicating available positions (1 = available, 0 = blocked)
        gridWidth: Grid width
        gridHeight: Grid height
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Box Placement - Evolutionary Algorithm")
    
    widget = GridWidget(placement, mask, gridWidth, gridHeight)
    window.setCentralWidget(widget)
    
    window.show()
    app.exec()
