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
	if type(format_file) != dict: return []
	# get names of the data fields:
	data_names,data_parameters,format_name = scanDataFileTypes(format_file['types'])
	if not data_names: return []
	# add new keys: to the format_file dictionary:
	format_file['names'] = data_names
	format_file['parameters'] = data_parameters
	format_file['format'] = format_name



def scanDataFileTypes(types_list):
	""" Find and determine correct data_list from DataFileTypes.

	Args:
		types_list: List with names of types of the data
	Returns:
		data_names: List with names of data fields
		data_parameters: Dictionary where keys = data_names, and items = dictionary with standart structure
		format_name: name of the defined format current data file
	"""

	data_names = list()
	data_parameters = None
	data_parameters_template = {'SF':1, 'b0':0}
	format_name = 'undefined'
	storage = 'DataFileTypes.txt'

	# find appropriate with current format strings in file and then 
	# search around this strings name and options of this  format
	
	# get data_names:
	# ---------------------
	with open(storage,'r') as f:
		ind = 0
		for line in f:
			ind += 1
			if re.search('F\s*=\s*\{', line):
				names = re.findall('\"([^\"]+)\"', line)
				if len(names) == len(types_list):
					data_names = names
					ind = ind-3
					break
	if not data_names:
		j = 0
		for i in types_list:
			j += 1
			data_names.append('Var'+str(j)+'_'+i)
	# build data_parameters
	# ---------------------
	data_parameters = dict.fromkeys(data_names)
	for i in data_parameters.keys():
		data_parameters[i] = data_parameters_template
	# get  format name
	# ---------------------
	with open(storage,'r') as f:
		for i, line in enumerate(f):
			if i == ind:
				s = re.search('\w+', line)
				format_name = s.group()
				# get all defined options for this format
				options_list = list()
				line = f.readline()
				while line:
					print(f.readline())
					options_list.append(line)
				break



	return data_names, data_parameters, format_name


def recognize(format_file):

	""" Recognize current data file by dictionary D that return from scanFile
		Return list with field names of the data in current file 
	"""

	DataList = ''

	# recognizing existing data type
	# ------------------------------------------------------
	ls = ['int', 'int', 'float', 'float', 'float', 'float', 'float', 'float', 'int']
	if format_file['types'] == ls:
		data_name = 'grom_TM01'
	return DataList

