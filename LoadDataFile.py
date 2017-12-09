# -*- coding: utf-8 -*-
"""
This module provides a load experimental data from files. 
"""

import numpy as np
import os
import ScanDataFile, ReadDataFile
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import webbrowser

class LoadDataFile:
	""" The class provides load data from file."""

	adress = ''
	file_format = None
	data = None
	def __init__(self, *argv):
		# get correct adress with GUI 	
		if not argv: 
			self.adress = self.open_file_GUI("")
		else:
			self.adress = self.open_file_GUI(argv[0])
		if not self.adress:
			return
		# recognizing file format
		self.file_format = ScanDataFile.scan_file(self.adress)
		# reading data
		if self.file_format['read']:
			self.data = ReadDataFile.read(self.file_format)



	def open_file_GUI(self, arg):
		"""  Call GUI OpenFileDialog and return the correct pathname.

		Args:
			arg: File name, or path, or empty.
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


	def info(self):
		data = self.file_format
		f = open('info.txt','w')
		f.close()
		webbrowser.open('info.txt')



