import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QDesktopWidget,
							 QHBoxLayout, QSplitter, QFrame, QSplitter, QStyleFactory,
							 QTextEdit,QWidget,QVBoxLayout,QSlider)
from PyQt5.QtGui import QIcon
from LoadDataFile import LoadDataFile
from PyQt5.QtCore import Qt

class Analyzer(QWidget):

	def __init__(self):
		super().__init__()

		self.title = 'Gravi.Analyzer'
		self.resize(1000, 700)
		self.setWindowTitle(self.title)
		self.setWindowIcon(QIcon('icon.png'))
		self.center()
		self.show()
		
		hbox = QHBoxLayout()

		# -----------------------------
		# Plot layout 
		# -----------------------------
		slider_box = QVBoxLayout()
		slider1 = QSlider(Qt.Horizontal)
		slider2 = QSlider(Qt.Horizontal)
		slider_box.addWidget()

		leftside_plot = QFrame()
		leftside_plot.setFrameShape(QFrame.StyledPanel)
		leftside_slider = QFrame()
		leftside_slider.setFrameShape(QFrame.StyledPanel)
		# -----------------------------


		rightside = QFrame()
		rightside.setFrameShape(QFrame.Panel | QFrame.Raised)
		rightside.setLineWidth(2)
		bottomside = QFrame()
		bottomside.setFrameShape(QFrame.StyledPanel)

		plot_split = QSplitter(Qt.Vertical)
		plot_split.addWidget(leftside_plot)
		plot_split.addWidget(leftside_slider)
		plot_split.setSizes([650,50])
		ver_split = QSplitter(Qt.Horizontal)
		ver_split.addWidget(plot_split)
		ver_split.addWidget(rightside)
		ver_split.setSizes([700,300])

		hor_split = QSplitter(Qt.Vertical)
		hor_split.addWidget(ver_split)
		hor_split.addWidget(bottomside)
		hor_split.setSizes([600,100])
		hbox.addWidget(hor_split)

		self.setLayout(hbox)
		QApplication.setStyle(QStyleFactory.create('cleanlooks'))

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Analyzer()
	sys.exit(app.exec_())