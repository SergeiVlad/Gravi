import sys, os
import ntpath
from PyQt5.QtWidgets import (QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,
                             QPushButton, QDesktopWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                             QMainWindow, QListWidget, QListWidgetItem, QErrorMessage)
from PyQt5.QtGui import QIcon
from LoadDataFile import LoadDataFile
import ScanDataFile
from ViewData import ViewData

 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Gravi'
        self.resize(550, 400)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
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
        self.btn1 = QPushButton("Info")
        self.btn1.setObjectName("Info")
        self.btn2 = QPushButton("View")
        self.btn2.setObjectName("View")
        self.lst1 = QListWidget()
        for item in files_history:
            self.lst1.addItem(item)
        self.btn1.clicked.connect(self.openFileNameDialog)
        self.btn2.clicked.connect(self.openFileNameDialog)
        self.tab1.layout.addWidget(self.lst1)
        self.tab1.layout.addWidget(self.btn1)
        self.tab1.layout.addWidget(self.btn2)
        self.tab1.setLayout(self.tab1.layout)

        # Create tab 2
        self.tab2.layout = QVBoxLayout(self)
        self.btn1 = QPushButton("Info")
        self.btn1.setObjectName("Info")
        self.btn2 = QPushButton("View")
        self.btn2.setObjectName("View")
        self.lst2 = QListWidget()
        for item in path_history:
            self.lst2.addItem(item)
        self.btn1.clicked.connect(self.openFileNameDialog)
        self.btn2.clicked.connect(self.openFileNameDialog)
        self.tab2.layout.addWidget(self.lst2)
        self.tab2.layout.addWidget(self.btn1)
        self.tab2.layout.addWidget(self.btn2)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.layout2 = QHBoxLayout()        
        #Initialize tab screen
        self.tabs_2 = QTabWidget()
        self.tab1_2 = QWidget()
        self.tab2_2 = QWidget()
        self.tabs.resize(300, 200)
        # Add tabs
        self.tabs_2.addTab(self.tab1_2, "Files")
        self.tabs_2.addTab(self.tab2_2, "Dir")
        # Add tabs to widget
        self.layout2.addWidget(self.tabs_2)
        self.setLayout(self.layout2)


    def openFileNameDialog(self):
        # Get adress from tab lists:
        if self.tabs.tabText(self.tabs.currentIndex()) == 'Files':
            if self.lst1.currentItem():
                fileName = self.lst1.currentItem().text()
            else:
                fileName = self.filepath
        elif self.tabs.tabText(self.tabs.currentIndex()) == 'Dir':
            if self.lst2.currentItem():
                fileName = self.lst2.currentItem().text()
            else:
                fileName = self.filepath
        # Check adress and set default dir if it not exist
        if not os.path.isfile(fileName) and not os.path.isdir(fileName):
            fileName = self.filepath

        # Load file 
        if os.path.isdir(fileName):
            fileName, _ = QFileDialog.getOpenFileName(self,"Select file for load", directory = fileName)

        # Get and sort history, refresh tab lists:
        if os.path.isfile(fileName):
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

            # Processing file:
            # ----------------------------------------------
            current_button = self.sender()
            if current_button.objectName() == "Info":
                try:
                    A = ScanDataFile.scan_file(fileName)
                    ScanDataFile.info(A)
                except:
                    pass
            # -----------------------------------------------
            if current_button.objectName() == "View":
            	try:
	                A = LoadDataFile(fileName)
	                if A.file_format['read']:
	                    self.wnd = ViewData(A)
	                    self.wnd.initUI()
	                    self.wnd.show()
	                else:
	                    err = QErrorMessage(self)
	                    err.showMessage('Unreadable format of the file.')
            	except:
                    err = QErrorMessage(self)
                    err.showMessage('Can not read this file.')


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