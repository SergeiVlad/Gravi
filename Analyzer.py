import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QDesktopWidget,
							 QHBoxLayout, QSplitter, QFrame, QSplitter, QStyleFactory,
							 QTextEdit,QWidget,QVBoxLayout,QSlider,QLineEdit,
							 QLabel,QGridLayout,QPushButton,QTextEdit,QTabWidget,qApp,
							 QAction,QMenu,QTreeView,QListWidget,QComboBox)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
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

		# Tab Browser
		# ------------------------
		cLayout = QVBoxLayout()
		lst_file = QListWidget()
		lst_file.addItem('Not files yet')
		lst_file.addItem('Not files yet')
		lst_file.addItem('Not files yet')
		lst_dir = QListWidget()
		lst_dir.addItem('Not dirs yet')
		lst_dir.addItem('Not dirs yet')
		lst_dir.addItem('Not dirs yet')
		tab_files = QTabWidget()
		tab_files.addTab(lst_file,'Files')
		tab_files.addTab(lst_dir,'Directories')
		cLayout_btn = QHBoxLayout()
		btn_load = QPushButton('Load')
		btn_info = QPushButton('Info')
		btn_prev = QPushButton('Preview')
		cLayout_btn.addWidget(btn_load)
		cLayout_btn.addWidget(btn_info)
		cLayout_btn.addWidget(btn_prev)
		lbl_hist = QLabel('Load data files history')
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

		cLayout.addWidget(lbl_hist)
		cLayout.addWidget(tab_files)
		cLayout.addLayout(cLayout_btn)
		cLayout.addWidget(lbl_obj)
		cLayout.addWidget(b_tree)
		cFrame1 = QFrame()
		cFrame1.setLayout(cLayout)
		control_tab.addTab(cFrame1,'Browser')

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
		wLayout2.addWidget(QPushButton('four'))
		wLayout2.addWidget(QPushButton('five'))
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







if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = AnalyzerMain()
	sys.exit(app.exec_())