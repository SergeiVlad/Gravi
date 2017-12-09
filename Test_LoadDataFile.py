import unittest
from LoadDataFile import LoadDataFile

class Test_LoadDataFile(unittest.TestCase):
	"""docstring for Test_LoadDataFile"""

	# testing by init object without argument 
	# def test_LoadDataFile_get_adress(self):
	# 	tt = LoadDataFile('/home/segrii/dev/Gravi/')

if __name__ == '__main__':
	tt = LoadDataFile('/home/segrii/dev/Gravi/test2.txt')
	tt.file_format['format']
	tt.file_format['parameters']
	# unittest.main(exit = False)