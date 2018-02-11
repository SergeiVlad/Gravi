""" Load sensors data from files to RAM."""

import os
import ScanDataFile, ReadDataFile
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import webbrowser
import matplotlib.pyplot as plt

class LoadDataFile:
	""" Provides load data from file to RAM.  """
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
		"""
		Show data information in the default TextEditor.
		"""
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
			if 'names' in data:
				f.write('%s\t%-s\n'% ('data names: ',data['names']))
			if 'types' in data:
				f.write('%s\t%-s\n'% ('data types: ',data['types']))
			f.write('%-s\n' % ('-------------------------------'))
			if 'parameters' in data:
				if isinstance(data['parameters'], dict):
					f.write('%s\n' % 'parameters:')
					for i in data['parameters'].keys():
						f.write('\t%-s:\t%-s\n' % (i, data['parameters'][i]))
				else:
					f.write('%s\n' % 'parameters:')
					f.write('\t%s\n' % 'not parameters.')

			try:
				f.write('%-s\n' % ('-------------------------------'))
				with open(data['filename']) as b:
					i = 0
					while i < data['col'] or i < 10:
						s[i] = b.readline()
						f.write('%-s' % s)
						i += 1
				f.write('%s\n' % 'first rows:')
				f.write('%-s\n' % ('-------------------------------'))
				for i in range(len(s)):
					f.write('%-s' % s[i])
			except: 
				f.write('%s\n' % 'first rows:')
				f.write('\t%s' % 'unreadable file.')

			webbrowser.open('info.txt')

	def set_param(self):
		"""
		Open DataFileTypes.txt for edit and save new parameters.
		"""
		webbrowser.open('DataFileTypes.txt')
		self = self.__init__(self.adress)

	def get(self,signal):
		""" Get data vector by signal name.  

			Args:
				signal - string with data name
		"""
		return self.data[signal]

	def signals(self):
		"""
		Show all available signals in shell.
		"""
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