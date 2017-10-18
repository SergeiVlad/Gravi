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
		sep - separator. Defautl separator is \\t
		hex - if hexadecimal numbers are present in data
		types - list of the each rows types
	"""
	# initialisation D:
	D = {'read':False, 
		'col':0, 
		'row':0,
		'nhead':0, 
		'coleq':1, 
		'tact_fq':1, 
		'sep':'\\t', 
		'hex':False,
		'types':[]}
	ine_str = None
	ind = None 
	ind_prew = None

	# Raw count
	with open(fname) as f:
	    D['raw'] = sum(1 for _ in f)
	    
	if D['row'] < 5:
		break

	# Head recognize
	with open(fname) as f:
		# init firs line parameters
		line_str = f.readline()
		types_list = types_recognize(line_str)
		types_calc = calc_type_list(types_list)
		if types_calc['str'] > 0:
			# check next lines:

			line_str = f.readline()
			types_list = types_recognize(line_str)
			types_calc = calc_type_list(types_list)




	# Head & hex recognize 
	with open(fname, 'r') as f:
		line_str = f.readline()
		if line_str:
			D['read'] = True
		try: 
			pdb.set_trace()
			types_list = types_recognize(line_str)
			types_calc = calc_type_list(types_list)
			num = len(np.array(line_str.split(),'float'))
			D['col'] = num
		except:
			# head identation:
			D['nhead'] = 1
			for i in range(5):
				try:
					line_str = f.readline()
					line_lst = line_str.split()
					np_arr = np.array(line_lst,'float')
					break
				except:
					D['nhead'] += 1
			# another head identation for hexadecimal numbers in rows:
			if D['nhead'] >= 5:
				f.seek(0,0)
				D['nhead'] = 0
				# First attempt to find hexadecimal numbers in first row
				line_str = f.readline()
				line_lst = line_lst.split()
				line_arr = []
				for i in range(len(line_lst)):
					try:
						line_arr.append(int(line_lst[i],16))
					except ValueError:
						line_arr.append('')
				if any(line_arr): # if first attempt is successful search will end
					D['nhead'] = 0
					D['hex'] = True
					ind_prew = next(i for i,j in enumerate(line_arr) if j)
				else: # find another strings with hexadecimal elements
					D['nhead'] = 1 
					for i in range(9):
						# in this loop we try to get hex numbers from string parts
						# if str part is not hex element it = '', else element = int number 
						try:
							line_str = f.readline()
							line_lst = line_lst.split()
							line_arr = []
							for j in range(len(line_lst)):
								try: line_arr.append(int(line_lst[i],16))
								except ValueError: 	line_arr.append('')
						except: # break cycle 'for' if can't recognize string parts
							D['read'] = False
							break
						# check results of hexadecimal scaning in line_arr by two criteries
						# 1) if any in array is non empty
						# 2) if nonepty element inex is equal to previous el index
						try: ind = next(i for i,j in enumerate(line_arr) if j)
						except: ind = ''
						if (not not ind) & (ind == ind_prew):
							D['hex'] = True
						elif (not ind):
							D['nhead'] += 1
							D['hex'] = False
							break
			# head number check:
			if D['nhead'] >=5:
				D['read'] = False

	# Column recoqnize
	with open(fname, 'r') as f:
		for i in range(D['nhead']):
			line_str = f.readline()
			
		line_str = f.readline()
		type_lst = types_recognize(line_str)
		D['col'] = len(type_lst)
		D['types'] = type_lst

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


if __name__ == '__main__':

	D  = scan('I:/PROGS/Python/work/Gravi/test2.txt')