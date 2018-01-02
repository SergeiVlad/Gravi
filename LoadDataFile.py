# -*- coding: utf-8 -*-
"""
This module provides a load experimental data from files. 
"""

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
		""" Show data information """
		data = self.file_format
		with open('info.txt','w') as f:
			f.write('adress:\t%s\n' % (self.adress))
			f.write('format:\t%s\n' % (data['format']))
			f.write('%-s\t%-s\n' % ('length:',data['row']))
			f.write('%-s\t%-s\n' % ('columns:',data['col']))
			f.write('%-s\t%-s\n' % ('frequency:',data['tact_fq']))
			f.write('%-s\t%-s\n' % ('head rows:',data['nhead']))
			if data['read']:
				f.write('%-s\t%-s\n' % ('readability:','True'))
			else:
				f.write('%-s\t%-s\n' % ('readability:','False'))
			if 'types' in data:
				f.write('%s\t%-s\n'% ('data types: ',data['types']))
			f.write('%-s\n' % ('-------------------------------'))
			if 'parameters' in data:
				if isinstance(data['parameters'], dict):
					f.write('%s\n' % 'parameters:')
					for i in data['parameters'].keys():
						f.write('\t%-s:\t%-s\n' % (i, data['parameters'][i]))
			webbrowser.open('info.txt')
			f.write('%-s\n' % ('-------------------------------'))
			f.write('%s\n' % 'first 10 rows:')
			with open(data['filename']) as b:
				i = 0
				while i < data['col'] or i < 10:
					s = b.readline()
					f.write('%-s' % s)
					i += 1

	def set_param(self):
		""" Open DataFileTypes.txt for edit and save new parameters """
		webbrowser.open('DataFileTypes.txt')
		self = self.__init__(self.adress)

