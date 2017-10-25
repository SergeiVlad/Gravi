import numpy as np
import openFileDialog as ofd
import os
import scanFile
import pdb
import sys

# fname = ofd.fopen('E:/ИСПЫТАНИЯ/УКННС/termo/20_m20_p85/')
# fname = ofd.fopen('I:/PROGS/Python/work/Gravi/test.txt')
# fname = ofd.fopen('I:/PROGS/Python/work/Gravi/test2.txt')
fname = ofd.fopen('/media/segrii/Transcend/PROGS/Python/work/Gravi/test1.txt')


if type(fname) == str:
	# pdb.set_trace()
	sPath, sFile  = os.path.split(fname)
	if not sPath or not sFile:
		sys.exit(0)

	# D is a dictionary
	D = scanFile.scan(fname)

	# D is a dictionary with data
	D = readDataFile.read(D)

	""" This script loadDataFile must be in future as method in class
	imsu - inertial measurement sensors and units, D is an object of this class 
	And loadDataFile py must be in the __init__ method of the object D """

	# Print method for future class imsu
	for i in D.keys():
		print(i,':',D[i])

