import unittest
from LoadDataFile import LoadDataFile

class Test_LoadDataFile(unittest.TestCase):
	"""docstring for Test_LoadDataFile"""

	# test head
	# -----------------------------------------------------------
	def test_ScanFile_for_head_number_1(self):
		expected_head = 4
		adress = 'test1.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])
	def test_ScanFile_for_head_number_2(self):
		expected_head = 1
		adress = 'test2.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])
	def test_ScanFile_for_head_number_3(self):
		expected_head = 7
		adress = 'test3.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])
	def test_ScanFile_for_head_number_4(self):
		expected_head = 0
		adress = 'test4.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_head, data.file_format['nhead'])

	# test columns
	# -----------------------------------------------------------
	def test_ScanFile_for_column_number_1(self):
			expected_column = 9
			adress = 'test1.txt'
			data = LoadDataFile(adress)
			self.assertEqual(expected_column, data.file_format['col'])
	def test_ScanFile_for_column_number_2(self):
			expected_column = 10
			adress = 'test2.txt'
			data = LoadDataFile(adress)
			self.assertEqual(expected_column, data.file_format['col'])
	def test_ScanFile_for_column_number_3(self):
			expected_column = 16
			adress = 'test3.txt'
			data = LoadDataFile(adress)
			self.assertEqual(expected_column, data.file_format['col'])
	def test_ScanFile_for_column_number_4(self):
			expected_column = 52
			adress = 'test4.txt'
			data = LoadDataFile(adress)
			self.assertEqual(expected_column, data.file_format['col'])	

if __name__ == '__main__':
	unittest.main(exit = False)			