import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

def fopen(*args):

	"""Call GUI OpenFileDialog and return the pathname """

	path = ''

	if len(args)>0:
		if type(args[0]) == str:
			path = args[0]

	if os.path.isfile(path):
		return(path)


	app = QApplication(sys.argv)
	w = QWidget()
	# options  = QFileDialog.Options()
	# options |= QFileDialog.DontUseNativeDialog
	# fileName, _ = QFileDialog.getOpenFileName(w,"Open file", options=options)
	if os.path.isdir(path):
		fileName, _ = QFileDialog.getOpenFileName(w,"Open file", directory = path)
	else:
		fileName, _ = QFileDialog.getOpenFileName(w,"Open file",'')
	# w.show()
	# sys.exit(app.exec_())
	
	return fileName