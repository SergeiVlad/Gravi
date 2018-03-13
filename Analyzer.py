import sys, os
import ntpath
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QDesktopWidget,
							 QHBoxLayout, QSplitter, QFrame, QSplitter, QStyleFactory,
							 QTextEdit,QWidget,QVBoxLayout,QSlider,QLineEdit,
							 QLabel,QGridLayout,QPushButton,QTextEdit,QTabWidget,qApp,
							 QAction,QMenu,QTreeView,QListWidget,QComboBox, QFileDialog)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from LoadDataFile import LoadDataFile
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random
import numpy as np
from LoadDataFile import LoadDataFile
import ScanDataFile
from ViewData import ViewData

class AnalyzerMain(QMainWindow):
	def __init__(self):

		super().__init__()
		self.analyzerWidget = AnalyzerWidget()
		self.setCentralWidget(self.analyzerWidget)
		self.title = 'Gravi.Analyzer'
		self.resize(1100, 600)
		self.setWindowTitle(self.title)
		self.setWindowIcon(QIcon('icon.png'))
		self.center()
		self.statusBar().showMessage('Project under development')

		# Menu Bar
		# ---------------------------
		menuBar = self.menuBar()
		FileMenu = menuBar.addMenu('&File')
		# submenus:
		mClear = QAction('Clear workspace',self)
		mSave = QAction('Save workspace',self)
		mLoad = QAction('Load workspace',self)
		FileMenu.addAction(mSave)
		FileMenu.addAction(mLoad)
		FileMenu.addAction(mClear)
		ToolsMenu = menuBar.addMenu('&Tools')
		mHistory = QAction('Open history file',self)
		mFileTypes = QAction('Open Data types settings',self)
		ToolsMenu.addAction(mHistory)
		ToolsMenu.addAction(mFileTypes)
		ExitMenu = menuBar.addMenu('Exit')
		mExit = QAction('Quit without save session',self)
		ExitMenu.addAction(mExit)

		# Tool Bar:
		# ---------------------------
		new_fig = QAction(QIcon('new_window.png'),'Figure',self)
		zoom_in = QAction(QIcon('zoom_in.png'),'Zoom in',self)
		zoom_out = QAction(QIcon('zoom_out.png'),'Zoom out',self)
		vertical_zoom = QAction(QIcon('vertical_zoom.png'),'Vertical zoom',self)
		horizontal_zoom = QAction(QIcon('horizontal_zoom.png'),'Horizontal zoom',self)
		default_zoom = QAction(QIcon('default_view.png'),'Default size',self)
		self.toolbar = self.addToolBar('Figure')
		self.toolbar.addAction(new_fig)
		self.toolbar.addAction(zoom_in)
		self.toolbar.addAction(zoom_out)
		self.toolbar.addAction(vertical_zoom)
		self.toolbar.addAction(horizontal_zoom)
		self.toolbar.addAction(default_zoom)

		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

class AnalyzerWidget(QWidget):

	def __init__(self):
		super().__init__()
		hbox = QHBoxLayout()

		# -----------------------------
		# Create frames
		# -----------------------------

		# 1. Plot frame:
		plotFrame = QFrame()
		plotFrame.setFrameShape(QFrame.Panel| QFrame.Raised)
		plotFrame.setStyleSheet(self.stylesheet_qframe1())
		figure = plt.figure()
		canvas = FigureCanvas(figure)
		ln = 100000;
		data = [random.random() for i in range(ln)]
		data = np.cumsum(data-np.mean(data))
		ax = figure.add_subplot(111)
		plt.subplots_adjust(left=0.00,bottom=0.002,right=1,top=1,wspace=0,hspace=0)
		ax.plot(data)
		ax.grid()
		ax.set_facecolor('#C4C4C4')
		ax.grid(color='#B80C09',linestyle = ':')
		plt.xlim([0,len(data)])
		canvas.draw()
		pLayout = QVBoxLayout()
		pLayout.addWidget(canvas)
		plotFrame.setLayout(pLayout)
		plotFrame.setContentsMargins(0,0,0,0)

		# 2. Horizontal sliders frame:
		sHbox = QVBoxLayout()
		slider1h = QSlider(Qt.Horizontal,self)
		slider1h.setStyleSheet(self.stylesheet_h())
		slider2h = QSlider(Qt.Horizontal,self)
		slider2h.setStyleSheet(self.stylesheet_h())
		sHbox.addWidget(slider1h)
		sHbox.addWidget(slider2h)
		sHbox.setSpacing(0)
		sHbox.setContentsMargins(1,0,1,0)
		sFrameH = QFrame()
		sFrameH.setFrameShape(QFrame.Panel | QFrame.Raised)
		sFrameH.setLayout(sHbox)

		# 3. Vertical sliders frame:
		sVbox = QHBoxLayout()
		slider1v = QSlider(Qt.Vertical,self)
		slider1v.setStyleSheet(self.stylesheet_v())
		slider2v = QSlider(Qt.Vertical,self)
		slider2v.setStyleSheet(self.stylesheet_v())
		sVbox.addWidget(slider1v)
		sVbox.addWidget(slider2v)
		sVbox.setSpacing(0)
		sVbox.setContentsMargins(1,0,1,0)
		sFrameV = QFrame()
		sFrameV.setFrameShape(QFrame.Panel| QFrame.Raised)
		sFrameV.setLayout(sVbox)

		# 4. SlidersControl frame:
		cornerFrame = QFrame()
		btnMax1 = QPushButton('max',cornerFrame)
		btnMax2 = QPushButton('max',cornerFrame)
		btnMax1.setGeometry(1,0,30,20)
		btnMax2.setGeometry(1,17,30,20)
		editMax1 = QLineEdit('0',cornerFrame)
		editMax2 = QLineEdit('0',cornerFrame)
		editMax1.setGeometry(31,0,60,20)
		editMax2.setGeometry(31,17,60,20)
		cornerFrame.setFrameShape(QFrame.Panel| QFrame.Raised)

		# 5. Control Panel frame:
		controlFrame = QFrame()
		controlFrame.setFrameShape(QFrame.Panel | QFrame.Raised)
		controlFrame.setLineWidth(2)
		control_tab = QTabWidget()
		cTab1 = QWidget()

		# Tab Browser
		# ------------------------
		cLayout1 = QVBoxLayout()
		cFrame1 = QFrame()
		self.lst_file = QListWidget()
		self.lst_dir = QListWidget()
		self.tab_files = QTabWidget()
		self.tab_files.addTab(self.lst_file,'Files')
		self.tab_files.addTab(self.lst_dir,'Directories')
		cLayout_btn = QHBoxLayout()
		self.btn_load = QPushButton('Load')
		self.btn_load.setObjectName('Load')
		self.btn_load.clicked.connect(self.openFileNameDialog)
		self.btn_info = QPushButton('Info')
		self.btn_info.setObjectName('Info')
		self.btn_info.clicked.connect(self.openFileNameDialog)
		self.btn_prev = QPushButton('Preview')
		self.btn_prev.setObjectName('Preview')
		self.btn_prev.clicked.connect(self.openFileNameDialog)

		# get open histories
		self.filepath = ''
		if os.path.exists('files_history.txt'):
			with open('files_history.txt', 'r') as f:
				files_history = f.read().splitlines()
			path_history = getPathList(files_history)
			self.filepath = path_history[0]
		else:
			files_history = list()
			path_history = list()
		for item in files_history:
			self.lst_file.addItem(item)
		for item in path_history:
			self.lst_dir.addItem(item)

		cLayout_btn.addWidget(self.btn_load)
		cLayout_btn.addWidget(self.btn_info)
		cLayout_btn.addWidget(self.btn_prev)
		lbl_hist = QLabel('Load data files history')
		cLayout1.addWidget(lbl_hist)
		cLayout1.addWidget(self.tab_files)
		cLayout1.addLayout(cLayout_btn)
		cFrame1.setLayout(cLayout1)
		
		lbl_obj = QLabel('Loaded objects')
		b_tree = QTreeView()
		b_tree.setAlternatingRowColors(True)
		b_tree_model = QStandardItemModel(0,5)
		b_tree_node = b_tree_model.invisibleRootItem()
		branch1 = QStandardItem("a")
		branch1.appendRow([QStandardItem("Child A"),None])
		childNode = QStandardItem("Child B")
		branch1.appendRow([childNode, None])
		branch2 = QStandardItem("b")
		branch2.appendRow([QStandardItem("Child C"),None])
		branch2.appendRow([QStandardItem("Child D"),None])
		branch3 = QStandardItem('c')
		branch4 = QStandardItem('d')

		b_tree_node.appendRow([ branch1, None])
		b_tree_node.appendRow([ branch2, None])
		b_tree_node.appendRow([ branch3, None])
		b_tree_node.appendRow([ branch4, None])

		b_tree.setModel(b_tree_model)
		b_tree_model.setHeaderData(0, Qt.Horizontal, 'Name')
		b_tree_model.setHeaderData(1, Qt.Horizontal, 'Type')
		b_tree_model.setHeaderData(2, Qt.Horizontal, 'Data')
		b_tree_model.setHeaderData(3, Qt.Horizontal, 'Size')
		b_tree_model.setHeaderData(4, Qt.Horizontal, 'Modified')
		b_tree.setColumnWidth(0,70)

		cLayout2 = QVBoxLayout()
		cLayout2.addWidget(lbl_obj)
		cLayout2.addWidget(b_tree)
		cFrame2 = QFrame()
		cFrame2.setLayout(cLayout2)

		cSplitBrowser = QSplitter(Qt.Vertical)

		cSplitBrowser.addWidget(cFrame1)
		cSplitBrowser.addWidget(cFrame2)
		cSplitBrowser.setSizes([200,50])

		cLayout = QVBoxLayout()
		cLayout.addWidget(cSplitBrowser)
		cLayout.setContentsMargins(0,0,0,0)

		# cLayout.addWidget(cFrame2)
		cFrame = QFrame()
		cFrame.setLayout(cLayout)
		control_tab.addTab(cFrame,'Browser')

		# Tab Work
		# -------------------------------
		wFrame1 = QFrame()
		wLayout = QGridLayout()
		wLbl_proc = QLabel('Process type')
		wComboBox1 = QComboBox()
		w_list = ["Signal view","Differentiation","Integration","Correlation",
				  "Allan variance","Fitting","Termo compensations","Calibration",
				  "Navigation","Fourier transform"]
		wComboBox1.setStyleSheet(self.stylesheet_combo2())
		wComboBox1.addItems(w_list)

		wFrame2 = QFrame()
		wFrame2.setFrameShape(QFrame.Box)
		wLayout.addWidget(wLbl_proc,0,0,1,1)
		wLayout.addWidget(wComboBox1,1,0,1,1)
		wLayout.addWidget(wFrame2,2,0,35,1)
		# Frame 2
		wLayout2 = QHBoxLayout()
		wLayout2.addWidget(QPushButton('one'))
		wLayout2.addWidget(QPushButton('two'))
		wLayout2.addWidget(QPushButton('three'))
		wLayout2.setAlignment(Qt.AlignTop)
		wLayout2.setSpacing(0)
		wFrame2.setLayout(wLayout2)

		wLayout.setContentsMargins(1,1,1,1)
		wFrame1.setLayout(wLayout)
		control_tab.addTab(wFrame1,'Work')
		
		# Tab Model
		# -------------------------------
		cTab3 = QWidget()
		control_tab.addTab(cTab3,'Model')

		control_layout = QVBoxLayout()
		control_layout.addWidget(control_tab)
		control_layout.setContentsMargins(0,0,0,0)
		controlFrame.setLayout(control_layout)
		
		# 6. Log panel:
		LogEdit = QTextEdit('>>')

		# -----------------------------
		# Split frames
		# -----------------------------

		# 1.  Plot + Vertical sliders:
		split1 = QSplitter(Qt.Horizontal)
		split1.addWidget(plotFrame)
		split1.addWidget(sFrameV)
		split1.setSizes([680,20])

		# 2.  Horizontal sliders + SlidersControl:
		split2 = QSplitter(Qt.Horizontal)
		split2.addWidget(sFrameH)
		split2.addWidget(cornerFrame)
		split2.setSizes([700,40])

		# 3.  1 + 2 :
		ver_split = QSplitter(Qt.Vertical)
		ver_split.addWidget(split1)
		ver_split.addWidget(split2)
		ver_split.setSizes([800,50])

		# 4.  3 + Control Panel:
		hor_split = QSplitter(Qt.Horizontal)
		hor_split.addWidget(ver_split)
		hor_split.addWidget(controlFrame)
		hor_split.setSizes([700,200])

		# 5.  4 + Log frame:
		bottom_split = QSplitter(Qt.Vertical)
		bottom_split.addWidget(hor_split)
		bottom_split.addWidget(LogEdit)
		bottom_split.setSizes([700,0])


		hbox.addWidget(bottom_split)

		self.setLayout(hbox)
		QApplication.setStyle(QStyleFactory.create('cleanlooks'))

	def openFileNameDialog(self):
		# Get adress from tab lists:
		if self.tab_files.tabText(self.tab_files.currentIndex()) == 'Files':
			if self.lst_file.currentItem():
				fileName = self.lst_file.currentItem().text()
			else:
				fileName = self.filepath
		elif self.tab_files.tabText(self.tab_files.currentIndex()) == 'Directories':
			if self.lst_dir.currentItem():
				fileName = self.lst_dir.currentItem().text()
			else:
				fileName = self.filepath
		# Check adress and set default dir if it not exist
		if not os.path.isfile(fileName) and not os.path.isdir(fileName):
			fileName = self.filepath
		# Load file 
		if os.path.isdir(fileName):
			fileName, _ = QFileDialog.getOpenFileName(self,"Select file for load", directory = fileName)

		print(fileName)
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
			self.lst_file.clear()
			self.lst_dir.clear()
			for currFilePath in files_history:
				self.lst_file.addItem(currFilePath)
			path_history = getPathList(files_history)
			for curPath in path_history:
				self.lst_dir.addItem(curPath)

			# Processing file:
			# ----------------------------------------------
			current_button = self.sender()
			if current_button.objectName() == "Info":
				try:
					A = ScanDataFile.scan_file(fileName)
					ScanDataFile.info(A)
				except:
					pass
			# # -----------------------------------------------
			if current_button.objectName() == "Preview":
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




	def stylesheet_h(self):
		return """
			QSlider::groove:horizontal {
				border: 1px solid #999999;
				height: 13px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
				background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
				margin: 2px 0;
			}

			QSlider::handle:horizontal {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
				border: 1px solid #5c5c5c;
				width: 26px;
				margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
				border-radius: 3px;
			}
		"""

	def stylesheet_v(self):
		return """
			QSlider::groove:vertical {
				border: 1px solid #999999;
				background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
				margin: 2px 0;
				width: 15px;
			}

			QSlider::handle:vertical {
				background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
				border: 1px solid #5c5c5c;
				height: 26px;
				margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
				border-radius: 3px;
			}
		"""

	def stylesheet_combo(self):
		return """
			QComboBox {
				 border: 1px solid gray;
				 border-radius: 3px;
				 padding: 1px 18px 1px 3px;
				 min-width: 6em;
			 }

			 QComboBox:editable {
				 background: white;
			 }

			 QComboBox:!editable, QComboBox::drop-down:editable {
				  background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
											  stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
											  stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
			 }

			 /* QComboBox gets the "on" state when the popup is open */
			 QComboBox:!editable:on, QComboBox::drop-down:editable:on {
				 background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
											 stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
											 stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
			 }

			 QComboBox:on { /* shift the text when the popup opens */
				 padding-top: 3px;
				 padding-left: 4px;
			 }

			 QComboBox::drop-down {
				 subcontrol-origin: padding;
				 subcontrol-position: top right;
				 width: 15px;

				 border-left-width: 1px;
				 border-left-color: darkgray;
				 border-left-style: solid; /* just a single line */
				 border-top-right-radius: 3px; /* same radius as the QComboBox */
				 border-bottom-right-radius: 3px;
			 }

			 QComboBox::down-arrow {
				 image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
			 }

			 QComboBox::down-arrow:on { /* shift the arrow when popup is open */
				 top: 1px;
				 left: 1px;
			 }
		"""

	def stylesheet_combo2(self):
		return """
			QComboBox QAbstractItemView {
				border: 2px solid darkgray;
				selection-background-color: lightgray;
			}
		"""


	def stylesheet_qframe1(self):
		return """
			QFrame::layout { margin: 0px }
			 
			QFrame {
				margin-top: 0px;
				margin-right: 0px;
				margin-bottom: 0px;
				margin-left: 0px;
				spacing: 0px;
				padding: 0px;
			}
		"""

def OpenFileDialog(st):
	print(st)

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
	ex = AnalyzerMain()
	sys.exit(app.exec_())