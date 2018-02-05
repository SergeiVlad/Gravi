import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,
                             QPushButton, QDesktopWidget, QTabWidget, QVBoxLayout, 
                             QMainWindow, QListWidget)
from PyQt5.QtGui import QIcon
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Gravi'
        self.resize(250, 400)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon2.png'))
        self.center()

        self.tab_widget = MytableWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MytableWidget(QWidget):
    """docstring for MytableWidget"""
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)        

        #Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Files")
        self.tabs.addTab(self.tab2, "Dir")

        # Create tab 1
        self.tab1.layout = QVBoxLayout(self)
        self.btn1 = QPushButton("Open")
        self.lst1 = QListWidget()
        self.btn1.clicked.connect(self.openFileNameDialog)
        self.tab1.layout.addWidget(self.lst1)
        self.tab1.layout.addWidget(self.btn1)
        self.tab1.setLayout(self.tab1.layout)

        # Create tab 2
        

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())