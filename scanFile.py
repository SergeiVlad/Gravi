""" Determine the type of data file for choose head string and features for read """
import numpy as np
import pdb


def scan(fname):

	""" 
	Di = scan(fname) - function get file path and return Data info dictionary D with fields:
		read - if True file could be read for processing, in other case - not
		col - number of columns
		row - number of rows
		nhead - number of head string
		coleq - show equal or not all strings, if coleq = true it mean that all strings are equal in the another case there are two type strings in data file: total and tact strings.
		tactf - show how many times occurs such string in relate to the total string. For example tactf = 200 mean that each 200th string will be a total. tact_col > 1 
		freq - show record frequency of the data
		sep - separator. Defautl separator jis \\t
		hex - if hexadecimal numbers are present in data
		types - list of the each rows types
	"""
	# initialisation D:
	D = {'read':False, 
		'col':0, 
		'row':0,
		'nhead':0, 
		'coleq':True, 
		'tact_fq':1, 
		'sep':'\\t', 
		'hex':False,
		'types':[]}

	# Raw count
	# --------------------------------------------------
	min_raw = 2 	# minimal number of lines in the file
	min_head = 5	# set minimal count for lines

	with open(fname) as f:
	    D['raw'] = sum(1 for _ in f)

	if D['row'] <= min_raw: 
		return D
	elif D['raw'] <= min_head: 
		nCount = D['raw']-1  
	else:
		nCount = 5

	# Head recognize
	# --------------------------------------------------
	with open(fname) as f:

		# analyze first line
		types_calc = analyze_line_types(f.readline())
		if types_calc['str'] > 0:
			D['nhead'] += 1
			# analyze next nCount lines:
			for i in range(nCount):
				types_calc = analyze_line_types(f.readline())
				if types_calc['str'] > 0:
					D['nhead'] += 1
	if D['row'] == D['nhead']:
		return D
	else:
		D['read'] = True


	# Hexadecimal recognize 
	# --------------------------------------------------
	with open(fname, 'r') as f:

		# skip head lines if it exist in file: 
		for i in range(D['nhead']):
			f.readline()

		types_calc = analyze_line_types(f.readline())
		if types_calc['hex'] > 0:
			D['hex'] = True


	# Columns recognize
	# --------------------------------------------------
	with open(fname, 'r') as f:

		# skip head lines if it exist in file: 
		for i in range(D['nhead']):
			f.readline()
			
		line_str = f.readline()
		types_lst = types_recognize(line_str)
		D['col'] = len(types_lst)
		D['types'] = types_lst

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
			ls_uneq.append(D['col'])

			for i in range(nQ):
				types_lst = types_recognize(f.readline())
				if len(types_lst) != D['col']:
					D['coleq'] = False
					n_uneq_lines += 1
					ls_uneq.append(len(types_lst))

			if n_uneq_lines > 0:
				D['col'] = list(set(ls_uneq))
				
	# frequency recognize
	# --------------------------------------------------
	if D['coleq'] == False:
		if n_uneq_lines > 4 & n_uneq_lines <= 6:
			D['takt_fq'] = 200
		if n_uneq_lines == 1 or n_uneq_lines == 2:
			D['takt_fq'] = 800
	else:
		D['coleq'] = 1

	return D


def types_recognize(line):

	# types_recognize(line) - return list with type names of the recognized data

	types_list = []

	ln_spl = line.split()

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
					types_list.append('hex')
				except ValueError:
					if ln_spl[i] != '': types_list.append('str')
					else: types_list.append('')

	return types_list


def calc_type_list(types_list):

	# calc_type_list - return dictionary with result of calculate each type of data from type_list

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
			if types_list[i] == '':
				type_calc['float'] += 1

	if any(x == 'hex' for x in types_list):
		for i in range(len(types_list)):
			if types_list[i] == 'hex':
				type_calc['hex'] += 1

	return type_calc	

def analyze_line_types(line):

	# analyze_types function get data line and return dict with types guantity

	types_list = types_recognize(line)
	types_count = calc_type_list(types_list)

	return types_count


if __name__ == '__main__':

	# D  = scan('I:/PROGS/Python/work/Gravi/test2.txt')
	D  = scan('/media/segrii/Transcend/PROGS/Python/work/Gravi/test2.txt')



