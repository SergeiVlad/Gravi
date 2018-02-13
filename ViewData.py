"""
View signals from data.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication)
from PyQt5.QtGui import QIcon
from LoadDataFile import LoadDataFile
from math import ceil

class ViewData(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowIcon(QIcon('icon.png'))
        self.data = LoadDataFile('test5.txt')
        names = self.data.file_format['names']
        max_row = 12
        columns = ceil(len(names)/max_row)

        for i in range(max_row*columns):
            if i >= len(names):
                names.append('')
        
        positions = [(i,j) for i in range(max_row) for j in range(columns)]
        
        for position, name, i in zip(positions, names, range(len(names))):
            if name == '':
                continue
            button = QPushButton(string(i)+'.'+name)
            button.setObjectName(name)
            button.clicked.connect(self.plotSignal)
            grid.addWidget(button, *position)
            
        self.move(300, 150)
        self.setWindowTitle('Signal View')
        self.show()
    
    def plotSignal(self):
        current_button = self.sender()
        self.data.plot(current_button.objectName())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ViewData()
    sys.exit(app.exec_())