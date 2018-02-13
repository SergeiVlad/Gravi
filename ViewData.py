"""
View signals from data.
"""

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QPushButton, QApplication)
from LoadDataFile import LoadDataFile

class ViewData(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)
        self.data = LoadDataFile('test5.txt')
        names = self.data.file_format['names']
        max_row = 10
        columns = int(len(names)/max_row)
        if columns < 1: columns = 1

        for i in range(max_row*columns):
            if i >= len(names):
                names.append('')
        
        positions = [(i,j) for i in range(max_row) for j in range(columns)]
        
        for position, name in zip(positions, names):
            
            if name == '':
                continue
            button = QPushButton(name)
            button.clicked.connect(self.plotSignal)
            grid.addWidget(button, *position)
            
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()
    
    def plotSignal(self):
        import pdb; pdb.set_trace()
        current_button = self.sender()
        print(current_button.objectName())
        self.data.plot('Gx')
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = ViewData()
    sys.exit(app.exec_())