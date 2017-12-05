# -*- coding: utf-8 -*-
""" 
ReadDataFile module read data after scaning file by ScanDataFile module. 
"""
import re

def read(format_file):
	""" Read data from file, work only with ScanDataFile output.

	Args:
		format_file: Dictionary from ScanDataFile methods.
	Returns:
		data: Dictionary with data vectors
	"""
	if type(format_file) != dict:
		return []

	data_list = scanDataFileTypes(format_file['types'])


def scanDataFileTypes(types_list):
	""" Find and determine correct data_list from DataFileTypes.

	Args:
		types_list: List with names of types of the data
	Returns:
		data_name_lits: List with names of data vectors
	"""

	data_name_list = list()
	find_type_res = list()
	with open('DataFileTypes.txt','r') as f:
		for line in f:
			if re.search('F\s*=\s*\{', line):
				names = re.findall('\"([^\"]+)\"', line)
				if len(names) == len(types_list):
					find_type_res.append(line)
	ind = 0 # index for chose format type in find_type_res list
	if not find_type_res:
		print('Find 0 access types. Data structure builded without defined names.')
		return None
	elif len(find_type_res)>1:
		print('Find',len(find_type_res),'types of formats.')
		print('Need to resolve problem of chose from find formats.')
		return None
	print('data_name_list defined.')
	data_name_list = find_type_res[ind]
	return data_name_list



def recognize(format_file):

	""" Recognize current data file by dictionary D that return from scanFile
		Return list with field names of the data in current file 
	"""

	DataList = ''

	# recognizing existing data type
	d# ------------------------------------------------------
	ls = ['int', 'int', 'float', 'float', 'float', 'float', 'float', 'float', 'int']
	if format_file['types'] == ls:
		data_name = 'grom_TM01'
	return DataList

