import unittest
from LoadDataFile import LoadDataFile

class Test_LoadDataFile(unittest.TestCase):
	"""docstring for Test_LoadDataFile 111"""

	def test_scanFile_head_1(self):
		expected_head = 4
		adress = '/home/segrii/dev/Gravi/test1.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])

	def test_scanFile_head_2(self):
		expected_head = 1
		adress = '/home/segrii/dev/Gravi/test2.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])

	def test_scanFile_head_3(self):
		expected_head = 8
		adress = '/home/segrii/dev/Gravi/test3.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])

if __name__ == '__main__':
	unittest.main(exit = False)