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
	
	# get names of the data fields:
	data_names,data_parameters,format_name = scanDataFileTypes(format_file['types'])
	if not data_names: return []
	# add new keys: to the format_file dictionary:
	format_file['names'] = data_names
	format_file['parameters'] = data_parameters
	format_file['format'] = format_name
	if format_file['read']:
		data = read_data(format_file)

def scanDataFileTypes(types_list):
	""" Find and determine correct data_list from DataFileTypes. If can't fidn determine own list.

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
					break
	if not data_names:
		j = 0
		for i in types_list:
			j += 1
			data_names.append('Var'+str(j)+'_'+i)
			return data_names, data_parameters, format_name
		
	# build data_parameters
	# ---------------------
	data_parameters = dict.fromkeys(data_names)
	for i in data_parameters.keys():
		data_parameters[i] = data_parameters_template.copy()

	# get  format name
	# ---------------------
	with open(storage,'r') as f:
		for i, line in enumerate(f):
			if i == ind-3:
				s = re.search('.+', line)
				format_name = s.group()
				break
	# get all defined options for this format
	# ----------------------
		options_strings = list()
		s = f.readline()
		while s and s != '\n':
			options_strings.append(s)
			s = f.readline()
	data_parameters = processing_option_strings(data_parameters, options_strings)

	return data_names, data_parameters, format_name

def processing_option_strings(data_parameters, options_strings):
	""" Recognize options for each data fields from otion_strings list

	Args:
		data_parameters: data_parameters dictionary where each field have data name and it options
		options_strings: list with strings from file which contand options information
	Returns:
		data_parameters: with uprade options for each data field
	"""

	# find the begin of the options:
	i = 0
	for line in options_strings:
		i += 1
		if re.search('^---', line):
			opts = options_strings[i+1:]
			break
	for line in opts:
		# scan for All
		if re.search('All\s*:', line):
			if re.search('All\s*:\s*(\w+)\s*=\s*-?\d',line):
				opt_names = re.findall('[:,]\s+(\w+)\s*=',line)
				opt_values = re.findall('[:,]\s+\w+\s*=\s*([-+]?[0-9]*\.?[0-9]*)',line)
			dp = data_parameters.keys()
			if opt_names and opt_values:
				for i in range(len(opt_values)):
					for j in range(len(dp)):
						data_parameters[list(data_parameters.keys())[j]][opt_names[i]] = float(opt_values[i])
		# scan for one
		if not re.search('All\s*:', line):
			sign = re.findall('([A-z,0-9]+)\s*:',line)[0]
			opt_names = re.findall('[:,]\s+(\w+)\s*=',line)
			opt_values = re.findall('[:,]\s+\w+\s*=\s*([-+]?[0-9]*\.?[0-9]*)',line)
			dp = list(data_parameters.keys())
			if opt_names and opt_values:
				for i in range(len(opt_values)):
					for j in range(len(dp)):
						if dp[j] == sign:
							data_parameters[dp[j]][opt_names[i]] = float(opt_values[i])
			# import pdb; pdb.set_trace()
	return data_parameters

def read_data(format_file):
	# import pdb; pdb.set_trace()
	data = np.textload(format_file['filename']) 
	return data