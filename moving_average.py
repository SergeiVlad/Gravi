# -*- coding: utf-8 -*-

"""Simple movinga average function without weight coefficients"""

import numpy as np
import matplotlib.pyplot as plt

def moving_average(a, n = 2):
	res = np.array([])
	for i in range(a.size-n+1):
		res = np.append(res, a[i:i+n].mean())
	for i in range(n-1):
		res = np.insert(res,0,res[0])
	return res
