""" readDataFile module read data after scaning file by scanFile module """
import re

def read(D):

	if type(D) == dict:
		data_name_list = scanDataFileTypes(D['types'])


def scanDataFileTypes():

	data_name_list = list()
	with open('DataFileTypes.txt','r') as f:
		# find 
		s = f.readline()

	return data_name_list
