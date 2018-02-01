""" ReadDataFile module read data as numpy vectors after scaning file by ScanDataFile module. """

import numpy as np
import re

def read(format_file):
	"""
	Read data from file, work only with ScanDataFile output. Sort data by signal names ind dict data. 

	Args:
		format_file: Dictionary from ScanDataFile methods.  
	Returns:
		data: Dictionary with data vectors.  
	"""
	data = {}

	if type(format_file) != dict: 
		return []
	
	if format_file['read']:
		names = format_file['names']
		types = format_file['types']
		
		# Define lambdas for convertor.  
		hex2int = lambda x: int(x,16)

		# build hex convertor
		conv = {}
		for i, ttype in enumerate(types):
			if ttype == 'hex':
				conv[i] = hex2int

		# import pdb; pdb.set_trace()
		# Read data from file.  
		D = np.loadtxt(format_file['filename'], skiprows = format_file['nhead'], converters = conv) 

		for index, (name, ttype) in enumerate (zip(names, types)):
			if ttype == 'int' or ttype == 'hex':
				data[name] = D[:,index].astype(int)
			else:
				data[name] = D[:,index]

	return data