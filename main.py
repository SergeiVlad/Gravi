import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,
                             QPushButton, QDesktopWidget, QTabWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Gravi'
        self.resize(250, 400)
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.center()

        btn = QPushButton('Open',self)
        btn.move(50, 50)
        self.openFileNameDialog()
 
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


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