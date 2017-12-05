import unittest
from LoadDataFile import LoadDataFile

class Test_LoadDataFile(unittest.TestCase):
	"""docstring for Test_LoadDataFile"""

	# testing by init object without argument 
	# def test_LoadDataFile_get_adress(self):
	# 	tt = LoadDataFile('/home/segrii/dev/Gravi/')

if __name__ == '__main__':
	tt = LoadDataFile('/home/segrii/dev/Gravi/test1.txt')
	# unittest.main(exit = False)