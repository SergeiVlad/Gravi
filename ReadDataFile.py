# -*- coding: utf-8 -*-
""" 
ReadDataFile module read data as numpy vectors after scaning file by ScanDataFile module. 
"""
import numpy as np
import re

def read(format_file):
	""" Read data from file, work only with ScanDataFile output.

	Args:
		format_file: Dictionary from ScanDataFile methods.
	Returns:
		data: Dictionary with data vectors
	"""

	if type(format_file) != dict: return []
	
	if format_file['read']:
		data = read_data(format_file)

def read_data(format_file):
	# import pdb; pdb.set_trace()
	data = []
	# data = np.loadtxt(format_file['filename'], skiprows = format_file['nhead']) 
	return data