import sys, os
import ntpath
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,
                             QPushButton, QDesktopWidget, QTabWidget, QVBoxLayout, 
                             QMainWindow, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QIcon
from LoadDataFile import LoadDataFile
 
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
        self.filepath = ''

        # Add tabs
        self.tabs.addTab(self.tab1, "Files")
        self.tabs.addTab(self.tab2, "Dir")

        # get open histories
        if os.path.exists('files_history.txt'):
            with open('files_history.txt', 'r') as f:
                files_history = f.read().splitlines()
            path_history = getPathList(files_history)
            self.filepath = path_history[0]
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
        self.lst1.currentItemChanged.connect(self.get_item1)
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
        self.lst2.currentItemChanged.connect(self.get_item2)
        self.tab2.layout.addWidget(self.lst2)
        self.tab2.layout.addWidget(self.btn2)
        self.tab2.setLayout(self.tab2.layout)    

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def get_item1(self):
        self.filepath = self.lst1.currentItem().text()
        print(self.filepath)

    def get_item2(self):
        self.filepath = self.lst2.currentItem().text()
        print(self.filepath)

    def openFileNameDialog(self):    
        """ Get adress from QWidgetList and open this file. Return data. """

        fileName = None
        data = None
        # check choose from QList
        if os.path.isfile(self.filepath) or os.path.isdir(self.filepath):
            data = LoadDataFile(self.filepath)
            fileName = self.filepath
        else:
            # Get opened filename, sort history from file and fill QWidgetList
            fileName, _ = QFileDialog.getOpenFileName(self,"Select file for load", directory = self.filepath)
        
        # get and sort history
        import pdb; pdb.set_trace()
        if fileName:
            # create files_history if it is not exits
            if not os.path.exists('files_history.txt'):
                with open('files_history.txt', 'w') as out:
                    out.write(fileName+'\n')
            else:
                # get all strings from history 
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

            # Open file with current filepath
            data = LoadDataFile(fileName)

        data.info()

        return data

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