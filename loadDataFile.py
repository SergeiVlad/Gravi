import numpy as np
import openFileDialog as ofd
import os
import scanFile


fname = ofd.fopen('E:/ИСПЫТАНИЯ/УКННС/termo/20_m20_p85/')
# fname = ofd.fopen('I:/PROGS/Python/work/Gravi/test.txt')
# fname = ofd.fopen('I:/PROGS/Python/work/Gravi/test2.txt')
# fname = ofd.fopen('/media/segrii/Transcend/PROGS/Python/work/Gravi/test.txt')


if type(fname) == str:

	sPath, sFile  = os.path.split(fname)

	D = scanFile.scan(fname)

	for i in D.keys():
		print(i,':',D[i])

