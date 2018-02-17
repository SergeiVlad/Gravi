""" Determine the type of the data file for choose features for its read."""
import numpy as np
import webbrowser
import re

def scan_file(fname):
	""" 
	Function get file path and return Data info dictionary.
	
	Args:
		fname: string with data path
	Returns:
		D: dictionary with fields:
			filename - pathname for data access
			read - if True file could be read for processing, in other case - not
			delim - delimiter  
			col - number of columns
			row - number of rows
			nhead - number of head string
			coleq - show equal or not all strings, if coleq = true it mean that all strings are equal in the another case there are two type strings in data file: total and tact strings.
			tactf - show how many times occurs such string in relate to the total string. For example tactf = 200 mean that each 200th string will be a total. tact_col > 1 
			freq - show record frequency of the data
			hex - if hexadecimal numbers are present in data
			types - list of the each rows types.
			names - names of the signals
			paramaters - specified in DataFileTypes.txt options for signals
			format - format name.
	"""
	# initialisation D:
	D = {'filename':'',
		'read':False,
		'delim':None,
		'col':0,
		'row':0,
		'format':'Undefined',
		'nhead':0, 
		'coleq':True, 
		'tact_fq':0, 
		'hex':False,
		'types':list(),
		'names':[],
		'parameters':[]}

	D['filename'] = fname

	# Row count
	# --------------------------------------------------
	min_row = 5 	# minimal number of lines in the file
	max_head = 25	# set maximum count for lines
	try:
		with open(fname) as f:
		    D['row'] = sum(1 for _ in f)
	except:
		return D

	if D['row'] <= min_row:
		return D
	elif D['row'] <= max_head:
		max_head = D['row']



	# Head recognize:
	# --------------------------------------------------
	with open(fname) as f:
		line = f.readline()
		types_list = types_recognize(line,D['delim'])
		types_count = analyze_line_types(line,D['delim'])
		types_count_prev = types_count
		for i in range(max_head):
			# conditions for define head strings
			condition_1 = types_count['str'] > 0  # if line have any strings
			condition_2 = line == '\n'			  # if line is empty
			# if deteсt hex words and previous line have another count of hex and int
			sub_condition_1 = types_count['int'] + types_count['hex']				# calc hex + int current
			sub_condition_2 = types_count_prev['int'] + types_count_prev['hex']	 	# calc hex + int prewious
			sub_condition_3 = types_count['hex'] > 0 and types_count_prev['str'] < 3 
			condition_3 = sub_condition_1 != sub_condition_2 and sub_condition_3
			if condition_1 or condition_2 or condition_3:
				D['nhead'] += 1
				# import pdb; pdb.set_trace()
			types_count_prev = types_count
			line = f.readline()
			types_list = types_recognize(line,D['delim'])
			types_count = analyze_line_types(line,D['delim'])

	if D['nhead'] == max_head:
	# Delimeter recognize:
	# --------------------------------------------------
		# try tp split data with delimiter "," 
		with open(fname) as f:
			res = []
			for i in range(max_head):
				line = f.readline()
				res.append(len(line.split(',')))
		b = list(i == res[-1] for i in res)
		if all(b):
			D['delim'] = ','
			D['read'] = True
			D['nhead'] = 0
		else:
			D['read'] = False
			return D
	else:
		D['read'] = True


	# Hexadecimal recognize 
	# --------------------------------------------------
	with open(fname, 'r') as f:
		# skip head lines if it exist in file: 
		for i in range(D['nhead']):
			f.readline()
		t = analyze_line_types(f.readline(),D['delim'])
		if t['hex'] > 0:
			D['hex'] = True

	# Columns recognize
	# --------------------------------------------------
	with open(fname, 'r') as f:
		# skip head lines if it exist in file: 
		for i in range(D['nhead']):
			f.readline()
		nLines = 20
		# get types list by first data line
		line_str = f.readline()
		types_lst_1 = types_recognize(line_str,D['delim'])
		D['col'] = len(types_lst_1)
		D['types'] = types_lst_1
		# find hex types that was hinden in first lines:
		# define number of the lines for testing for hiden hex
		if D['row'] < nLines + D['nhead']:
			nLines = D['row'] - D['nhead']


	# Ecuality in nQ columns recognize
	# --------------------------------------------------
	nQ = 1000
	if D['row'] > nQ + D['nhead']:
		with open(fname, 'r') as f:
			# skip head lines if it exist in file: 
			for i in range(D['nhead']):
				f.readline()
			# find unequality between data rows
			n_uneq_lines = 0
			ls_uneq = list()
			uqD = {str(D['col']):D['types']}
			ls_uneq.append(D['col'])

			for i in range(nQ):
				types_lst = types_recognize(f.readline(),D['delim'])
				if len(types_lst) != D['col']:
					D['coleq'] = False
					n_uneq_lines += 1
					ls_uneq.append(len(types_lst))
					uqD[str(len(types_lst))] = types_lst

			if n_uneq_lines > 0:
				D['col'] = list(set(ls_uneq))
				D['types'] = uqD

	# frequency recognize
	# --------------------------------------------------
	if D['coleq'] == False:
		if n_uneq_lines > 4 & n_uneq_lines <= 6:
			D['tact_fq'] = 200
		if n_uneq_lines == 1 or n_uneq_lines == 2:
			D['tact_fq'] = 800
	else:
		D['coleq'] = True

	# format, parameters and names recognize from DataFileTypes.txt	
	# ---------------------------------------------------
	data_names,data_parameters,format_name, options_strings = scanDataFileTypes(D['types'])
	if not data_names: return []
	# add new keys: to the format_file dictionary:
	D['names'] = data_names
	D['parameters'] = data_parameters
	D['format'] = format_name
	
	# check data types string
	# -------------------------------
	# import pdb; pdb.set_trace()
	D['types'] = checkDataTypes(D, options_strings)

	return D


def scanDataFileTypes(types_list):
	""" Find and determine correct data_list from DataFileTypes. If can't fidn determine own list.

	Args:
		types_list: List with names of types of the data
	Returns:
		data_names: List with names of data fields
		data_parameters: Dictionary where keys = data_names, and items = dictionary with standart structure
		format_name: name of the defined format current data file.
	"""
	data_names = list()
	data_parameters = None
	data_parameters_template = {'SF':1, 'b0':0}
	format_name = 'undefined'
	options_strings = list()
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
	# import pdb; pdb.set_trace()
	if not data_names:
		j = 0
		for i in types_list:
			j += 1
			data_names.append('Var'+str(j)+'_'+i)
		return data_names, data_parameters, format_name, options_strings
		
	# build data_parameters
	# ---------------------
	data_parameters = dict.fromkeys(data_names)
	for i in data_parameters.keys():
		data_parameters[i] = data_parameters_template.copy()

	# get format name
	# ---------------------
	with open(storage,'r') as f:
		for i, line in enumerate(f):
			if i == ind-3:
				s = re.search('.+', line)
				format_name = s.group()
				break

	# get all defined options for this format
	# ----------------------
		s = f.readline()
		while s and s != '\n':
			options_strings.append(s)
			s = f.readline()
			
	data_parameters = processing_option_strings(data_parameters, options_strings)

	return data_names, data_parameters, format_name, options_strings


def processing_option_strings(data_parameters, options_strings):
	""" Recognize options for each data fields from otion_strings list.

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

	return data_parameters

def checkDataTypes(D, options_strings):
	""" Check data types that was defined early, by read options from DataFileTypes.
	
	If DataFileTypes have options 'types' under current format name in next format:
		types = {6: 'hex'}
	function will change in D['formats'] list 7-th element on 'hex'.

	Args:
		D: dictionary with all ScanDataFile results.
		options_strings: list with strings from file which contand options information for current file
	Returns:
		formats: list with data types for refresh D['types']
	"""

	# initial data
	name_f = D['format']
	types = D['types']
	if name_f == 'undefined':
		return types
	# read option_strings and find current format options
	for line in options_strings:
		if re.search('types\s*=\s*{.+}', line):
			type_ind = re.findall('(\d+)\s*:', line)
			type_ind = list(map(int, type_ind))
			type_val = re.findall('\d+\s*:\s*\"(\w+)\"', line)
			if len(type_ind) == len(type_val):
				for i, ttype in enumerate(type_val):
					types[type_ind[i]-1] = type_val[i]

	return types

def types_recognize(line,delim):
	""" Return list with type names of the recognized data."""

	types_list = []

	ln_spl = line.split(delim)

	for i in range(len(ln_spl)):

		try: 
			int(ln_spl[i]) 
			types_list.append('int')
		except ValueError:
			try: 
				float(ln_spl[i])
				types_list.append('float')
			except ValueError:
				try: 
					int(ln_spl[i],16)
					if len(ln_spl[i])>3:
						types_list.append('hex')
					else:
						types_list.append('str')
				except ValueError:
					if ln_spl[i] != '': types_list.append('str')
					else: types_list.append('')
	return types_list

def calc_type_list(types_list):
	""" Return dictionary with result of calculate each type of data from type_list."""

	# initialisation type_calc:
	type_calc = {'str':0, 'int':0, 'float':0, 'hex':0}

	if any(x == 'str' for x in types_list):
		for i in range(len(types_list)):
			if types_list[i] == 'str':
				type_calc['str'] += 1

	if any(x == 'int' for x in types_list):
		for i in range(len(types_list)):
			if types_list[i] == 'int':
				type_calc['int'] += 1

	if any(x == 'float' for x in types_list):
		for i in range(len(types_list)):
			if types_list[i] == 'float':
				type_calc['float'] += 1

	if any(x == 'hex' for x in types_list):
		for i in range(len(types_list)):
			if types_list[i] == 'hex':
				type_calc['hex'] += 1

	return type_calc	

def analyze_line_types(line,delim):
	""" Analyze_types function get data line and return dict with types guantity. """
	types_list = types_recognize(line,delim)
	types_count = calc_type_list(types_list)
	return types_count


def info(data):
	""" Show data information in the default TextEditor. """
	
	with open('info.txt','w') as f:
		f.write('adress:\t%s\n' % (data['filename']))
		f.write('format:\t%s\n' % (data['format']))
		f.write('%-s\t%-s\n' % ('rows:',data['row']))
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
		if 'names' in data:
			f.write('%s\n' % 'String for DataFileTypes.txt:')	
			f.write('F = {')
			for i, name in enumerate(data['names']):
				f.write('%d: "%s", ' % (i+1, name) )
			f.write('}\n')
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
			f.write('%s\n' % 'first rows:')
			f.write('%-s\n' % ('============='))
			with open(data['filename']) as b:
				i = 0
				while i < data['col'] or i < 100:
					s = b.readline()
					f.write('%-s' % s)
					i += 1
		except: 
			f.write('%s\n' % 'stop reading file:')
			f.write('\t%s' % 'unreadable rows.')

		webbrowser.open('info.txt')


def read_file(format_file):
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
		delim = format_file['delim']
		
		# Define lambdas for convertor.  
		hex2int = lambda x: int(x,16)

		# build hex convertor
		conv = {}
		for i, ttype in enumerate(types):
			if ttype == 'hex':
				conv[i] = hex2int

		# import pdb; pdb.set_trace()
		# Read data from file.  
		D = np.loadtxt(format_file['filename'], skiprows = format_file['nhead'], converters = conv, delimiter = delim)

		for index, (name, ttype) in enumerate (zip(names, types)):
			if ttype == 'int' or ttype == 'hex':
				data[name] = D[:,index].astype(int)
			else:
				data[name] = D[:,index]

	return data