import numpy as np
import openFileDialog as ofd
import os
import scanFile


# fname = ofd.fopen('I:/PROGS/Python/work/Gravi/test.txt')
fname = ofd.fopen('/media/segrii/Transcend/PROGS/Python/work/Gravi/test.txt')



if type(fname) == str:

	sPath, sFile  = os.path.split(fname)

	D,s,ind,ind_prew = scanFile.scan(fname)

	for i in D.keys():
		print(i,':',D[i])


# KKKK1111a
