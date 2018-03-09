import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QDesktopWidget,
							 QHBoxLayout, QSplitter, QFrame, QSplitter, QStyleFactory,
							 QTextEdit,QWidget,QVBoxLayout,QSlider,QLineEdit,
							 QLabel,QGridLayout,QPushButton,QTextEdit,QTabWidget,qApp,
							 QAction,QMenu,QTreeView)
from PyQt5.QtGui import QIcon
from LoadDataFile import LoadDataFile
from PyQt5.QtCore import Qt

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
		self.statusBar().showMessage('Program under development')

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

		# 2. Horizontal sliders frame:
		sHbox = QVBoxLayout()
		slider1h = QSlider(Qt.Horizontal,self)
		slider1h.setStyleSheet(self.stylesheet_h())
		slider2h = QSlider(Qt.Horizontal,self)
		slider2h.setStyleSheet(self.stylesheet_h())
		sHbox.addWidget(slider1h)
		sHbox.addWidget(slider2h)
		sHbox.setSpacing(0)
		sHbox.setContentsMargins(1, 0, 1, 0)
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
		cTab2 = QWidget()
		cTab3 = QWidget()

		control_tab.addTab(cTab1,'Browser')
		control_tab.addTab(cTab2,'Work')
		control_tab.addTab(cTab3,'Model')
		control_layout = QVBoxLayout()
		control_layout.addWidget(control_tab)
		control_layout.setContentsMargins(0,0,0,0)
		controlFrame.setLayout(control_layout)
		
		# 6. Log panel:
		LogEdit = QTextEdit()

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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AnalyzerMain()
	sys.exit(app.exec_())