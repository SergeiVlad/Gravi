""" Load sensors data from files to RAM."""

import os
import ScanDataFile
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import webbrowser
import matplotlib.pyplot as plt


class LoadDataFile:
	""" Provides load data from file to RAM. """
	adress = ''
	file_format = None
	data = None
	def __init__(self, *argv):
		# Get correct adress with GUI.
		if not argv: 
			self.adress = self.open_file_GUI("")
		else:
			self.adress = self.open_file_GUI(argv[0])
		if not self.adress:
			return
		# Recognizing file format.
		self.file_format = ScanDataFile.scan_file(self.adress)
		# Reading data
		if self.file_format['read']:
			self.data = ScanDataFile.read_file(self.file_format)


	def open_file_GUI(self, arg):
		"""  Call GUI OpenFileDialog and return the correct pathname.  

		Args:
			arg: File name, or path, or  .
		Returns:
			fname: Absolute path for acces to data file.
		"""
		fname = ''
		if not arg:
			app = QApplication(sys.argv)
			w = QWidget()
			fname, _ = QFileDialog.getOpenFileName(w,"Open file")
		else:
			if os.path.isfile(arg):
				fname = arg
			elif os.path.isdir(arg):
				app = QApplication(sys.argv)
				w = QWidget()
				fname, _ = QFileDialog.getOpenFileName(w,"Open file", directory = arg)
			else:
				app = QApplication(sys.argv)
				w = QWidget()
				fname, _ = QFileDialog.getOpenFileName(w,"Open file")

		return fname


	def set_param(self):
		""" Open DataFileTypes.txt for edit and save new parameters. """
		webbrowser.open('DataFileTypes.txt')
		self = self.__init__(self.adress)


	def get(self,signal):
		""" Get data vector by signal name.  

			Args:
				signal - string with data name
		"""
		return self.data[signal]


	def signals(self):
		""" Show all available signals in shell. """
		print(self.file_format['names'])


	def plot(self, signal):
		"""
		Plot signal.  
		
		Args:
			signal - string signal name
			signal - list with signals names
		"""
		# import pdb; pdb.set_trace()
		if type(signal) == str:
			plt.plot(self.data[signal])
			plt.grid(True)
			plt.title(signal)
		elif type(signal) == list:
			y = {}
			fig, ax = plt.subplots(len(signal), sharey=False)
			for i, name in enumerate(signal):
				ax[i].plot(self.data[name])
				ax[i].set(title=name)
				ax[i].grid(True)

		plt.show()


	def info(self):
		""" Show data information in the default TextEditor. """

		return ScanDataFile.info(self.file_format)
