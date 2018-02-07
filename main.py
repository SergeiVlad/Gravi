import sys, os
import ntpath
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,
                             QPushButton, QDesktopWidget, QTabWidget, QVBoxLayout, 
                             QMainWindow, QListWidget, QListWidgetItem)
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
        self.layout = QVBoxLayout()        

        #Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Files")
        self.tabs.addTab(self.tab2, "Dir")

        # get open histories
        if os.path.exists('files_history.txt'):
            with open('files_history.txt', 'r') as f:
                files_history = f.read().splitlines()
            path_history = getPathList(files_history)
        else:
            files_history = list()
            path_history = list()

        # Create tab 1
        self.tab1.layout = QVBoxLayout(self)
        self.btn1 = QPushButton("Open")
        self.lst1 = QListWidget()
        for item in files_history:
            self.lst1.addItem(item)
        self.btn1.clicked.connect(self.openFileNameDialog)
        self.tab1.layout.addWidget(self.lst1)
        self.tab1.layout.addWidget(self.btn1)
        self.tab1.setLayout(self.tab1.layout)

        # Create tab 2
        self.tab2.layout = QVBoxLayout(self)
        self.btn2 = QPushButton("Open")
        self.lst2 = QListWidget()
        for item in path_history:
            self.lst2.addItem(item)
        self.btn2.clicked.connect(self.openFileNameDialog)
        self.tab2.layout.addWidget(self.lst2)
        self.tab2.layout.addWidget(self.btn2)
        self.tab2.setLayout(self.tab2.layout)    

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            # create files_history if it is not exits

            if not os.path.exists('files_history.txt'):
                with open('files_history.txt', 'w') as out:
                    out.write(fileName+'\n')
            else:
                # get all files from history 
                with open('files_history.txt', 'r') as f:
                    files_history = f.read().splitlines()
                # check file for exist in history
                if not fileName in files_history:
                    with open('files_history.txt', 'a') as f:
                        f.write(fileName+'\n')
                # sort history list by last open file
                with open('files_history.txt', 'r') as f:
                    files_history = f.read().splitlines()
                del files_history[files_history.index(fileName)]
                files_history.insert(0, fileName)

                with open('files_history.txt','w') as f:
                    for line in files_history:
                        f.write("%s\n" % line)
            self.lst1.clear()
            self.lst2.clear()
            for currFilePath in files_history:
                self.lst1.addItem(currFilePath)

            path_history = getPathList(files_history)
            for curPath in path_history:
                self.lst2.addItem(curPath)


def getPathList(files_history):
    """ Return path_history listh from files_history without repeated."""
    path_history = list()
    for item in files_history:
        curr_path = ntpath.dirname(item)
        if curr_path not in path_history:
            path_history.append(curr_path)

    return path_history


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())