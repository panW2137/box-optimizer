"""
GUI module for box packing optimization configuration.
Provides dialogs for parameter input and mask editing.
"""
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QFont


class MaskEditorWindow(QDialog):
    """Interactive mask editor - click cells to toggle availability."""
    
    def __init__(self, gridWidth, gridHeight, initialMask=None):
        super().__init__()
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellSize = 40
        
        # Initialize mask (1 = available, 0 = blocked)
        if initialMask:
            self.mask = [row[:] for row in initialMask]  # Deep copy
        else:
            self.mask = [[1] * gridWidth for _ in range(gridHeight)]
        
        self.setWindowTitle("Mask Editor - Click to Toggle Cells")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI with grid and buttons."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Instructions
        instructions = QLabel("Click cells to toggle: Green = Available, Red = Blocked")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        # Grid widget
        self.gridWidget = MaskEditorGrid(self.mask, self.gridWidth, self.gridHeight, self.cellSize)
        layout.addWidget(self.gridWidget)
        
        # Buttons
        buttonLayout = QHBoxLayout()
        
        clearButton = QPushButton("Clear All (All Available)")
        clearButton.clicked.connect(self.clear_mask)
        buttonLayout.addWidget(clearButton)
        
        doneButton = QPushButton("Done")
        doneButton.clicked.connect(self.accept)
        buttonLayout.addWidget(doneButton)
        
        layout.addLayout(buttonLayout)
    
    def clear_mask(self):
        """Reset mask to all available."""
        self.mask = [[1] * self.gridWidth for _ in range(self.gridHeight)]
        self.gridWidget.mask = self.mask
        self.gridWidget.update()
    
    def get_mask(self):
        """Return the configured mask."""
        return self.mask


class MaskEditorGrid(QWidget):
    """Interactive grid widget for mask editing."""
    
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
        """Draw the grid with colored cells."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw cells
        for i in range(self.gridHeight):
            for j in range(self.gridWidth):
                x = j * self.cellSize
                y = i * self.cellSize
                
                # Color based on mask value
                if self.mask[i][j] == 1:
                    color = QColor(144, 238, 144)  # Light green - available
                else:
                    color = QColor(255, 99, 71)  # Tomato red - blocked
                
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(color)
                painter.drawRect(x, y, self.cellSize, self.cellSize)
        
        # Draw grid lines
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        for i in range(self.gridHeight + 1):
            y = i * self.cellSize
            painter.drawLine(0, y, self.gridWidth * self.cellSize, y)
        
        for j in range(self.gridWidth + 1):
            x = j * self.cellSize
            painter.drawLine(x, 0, x, self.gridHeight * self.cellSize)
    
    def mousePressEvent(self, event):
        """Toggle cell on click."""
        x = event.pos().x() // self.cellSize
        y = event.pos().y() // self.cellSize
        
        if 0 <= x < self.gridWidth and 0 <= y < self.gridHeight:
            # Toggle mask value
            self.mask[y][x] = 1 - self.mask[y][x]
            self.update()


class ParameterWindow(QDialog):
    """Main window for configuring optimization parameters."""
    
    def __init__(self):
        super().__init__()
        
        # Default values
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
        
        # Initialize mask as all available
        self.mask = [[1] * self.defaults['gridWidth'] for _ in range(self.defaults['gridHeight'])]
        
        self.setWindowTitle("Box Packing Optimizer - Configuration")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the parameter input form."""
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
        # Title
        title = QLabel("Box Packing Optimization - Parameters")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(title)
        
        # Form layout for parameters
        formLayout = QFormLayout()
        
        # Create input fields
        self.inputs = {}
        
        # Random seed
        self.inputs['seed'] = QLineEdit(str(self.defaults['seed']))
        formLayout.addRow("Random Seed:", self.inputs['seed'])
        
        # Grid dimensions
        formLayout.addRow(QLabel(""))  # Spacer
        formLayout.addRow(QLabel("Grid Dimensions:"))
        self.inputs['gridWidth'] = QLineEdit(str(self.defaults['gridWidth']))
        formLayout.addRow("  Grid Width:", self.inputs['gridWidth'])
        self.inputs['gridHeight'] = QLineEdit(str(self.defaults['gridHeight']))
        formLayout.addRow("  Grid Height:", self.inputs['gridHeight'])
        
        # Box size constraints
        formLayout.addRow(QLabel(""))  # Spacer
        formLayout.addRow(QLabel("Box Size Constraints:"))
        self.inputs['minBoxWidth'] = QLineEdit(str(self.defaults['minBoxWidth']))
        formLayout.addRow("  Min Box Width:", self.inputs['minBoxWidth'])
        self.inputs['maxBoxWidth'] = QLineEdit(str(self.defaults['maxBoxWidth']))
        formLayout.addRow("  Max Box Width:", self.inputs['maxBoxWidth'])
        self.inputs['minBoxHeight'] = QLineEdit(str(self.defaults['minBoxHeight']))
        formLayout.addRow("  Min Box Height:", self.inputs['minBoxHeight'])
        self.inputs['maxBoxHeight'] = QLineEdit(str(self.defaults['maxBoxHeight']))
        formLayout.addRow("  Max Box Height:", self.inputs['maxBoxHeight'])
        
        # Algorithm parameters
        formLayout.addRow(QLabel(""))  # Spacer
        formLayout.addRow(QLabel("Algorithm Parameters:"))
        self.inputs['generations'] = QLineEdit(str(self.defaults['generations']))
        formLayout.addRow("  Generations:", self.inputs['generations'])
        self.inputs['populationSize'] = QLineEdit(str(self.defaults['populationSize']))
        formLayout.addRow("  Population Size:", self.inputs['populationSize'])
        self.inputs['mutationRate'] = QLineEdit(str(self.defaults['mutationRate']))
        formLayout.addRow("  Mutation Rate:", self.inputs['mutationRate'])
        self.inputs['boxCount'] = QLineEdit(str(self.defaults['boxCount']))
        formLayout.addRow("  Box Count:", self.inputs['boxCount'])
        
        mainLayout.addLayout(formLayout)
        
        # Buttons
        buttonLayout = QHBoxLayout()
        
        maskButton = QPushButton("Configure Mask")
        maskButton.clicked.connect(self.open_mask_editor)
        buttonLayout.addWidget(maskButton)
        
        startButton = QPushButton("Start Optimization")
        startButton.clicked.connect(self.validate_and_accept)
        startButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        buttonLayout.addWidget(startButton)
        
        mainLayout.addLayout(buttonLayout)
    
    def open_mask_editor(self):
        """Open the mask editor window."""
        try:
            gridWidth = int(self.inputs['gridWidth'].text())
            gridHeight = int(self.inputs['gridHeight'].text())
            
            if gridWidth <= 0 or gridHeight <= 0:
                raise ValueError("Grid dimensions must be positive")
            
            # Update mask size if grid dimensions changed
            if len(self.mask) != gridHeight or len(self.mask[0]) != gridWidth:
                self.mask = [[1] * gridWidth for _ in range(gridHeight)]
            
            # Open mask editor
            editor = MaskEditorWindow(gridWidth, gridHeight, self.mask)
            if editor.exec():  # If accepted
                self.mask = editor.get_mask()
                QMessageBox.information(self, "Mask Updated", "Mask configuration saved!")
        
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", 
                              f"Please enter valid grid dimensions.\nError: {str(e)}")
    
    def validate_and_accept(self):
        """Validate inputs and close dialog if valid."""
        try:
            self.get_parameters() # This will raise ValueError if invalid
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Parameters", str(e))
    
    def get_parameters(self):
        """Parse, validate and return parameters dictionary."""
        try:
            params = {}
            
            # Parse and validate all inputs
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
            
            # Validation
            if params['gridWidth'] <= 0 or params['gridHeight'] <= 0:
                raise ValueError("Grid dimensions must be positive")
            if params['minBoxWidth'] <= 0 or params['maxBoxWidth'] <= 0:
                raise ValueError("Box width constraints must be positive")
            if params['minBoxHeight'] <= 0 or params['maxBoxHeight'] <= 0:
                raise ValueError("Box height constraints must be positive")
            if params['minBoxWidth'] > params['maxBoxWidth']:
                raise ValueError("Min box width cannot exceed max box width")
            if params['minBoxHeight'] > params['maxBoxHeight']:
                raise ValueError("Min box height cannot exceed max box height")
            if params['generations'] <= 0:
                raise ValueError("Generations must be positive")
            if params['populationSize'] <= 0:
                raise ValueError("Population size must be positive")
            if not (0 <= params['mutationRate'] <= 1):
                raise ValueError("Mutation rate must be between 0 and 1")
            if params['boxCount'] <= 0:
                raise ValueError("Box count must be positive")
            
            return params
        
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}")

