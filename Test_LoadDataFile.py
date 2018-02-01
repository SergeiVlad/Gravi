import unittest
from LoadDataFile import LoadDataFile

class Test_LoadDataFile(unittest.TestCase):
	"""docstring for Test_LoadDataFile"""
	
	# test for names
	# -----------------------------------------------------------
	def test_ScanFile_name_test1_file(self):
		expected_name = 'Hartron type 9 columns'
		adress = 'test1.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_name, data.file_format['format'])		
	def test_ScanFile_name_test2_file(self):
		expected_name = 'Hartron type 10 columns'
		adress = 'test2.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_name, data.file_format['format'])		
	def test_ScanFile_name_test3_file(self):
		expected_name = 'undefined'
		adress = 'test3.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_name, data.file_format['format'])		
	def test_ScanFile_name_test4_file(self):
		expected_name = 'undefined'
		adress = 'test4.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_name, data.file_format['format'])		
	def test_ScanFile_name_test5_file(self):
		expected_name = 'UKNNS 71 columns'
		adress = 'test5.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_name, data.file_format['format'])		

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
	def test_ScanFile_uknns_col_number_5(self):
		expected_column = 71
		adress = 'test5.txt'
		data = LoadDataFile(adress)
		self.assertEqual(expected_column, data.file_format['col'])

if __name__ == '__main__':
	unittest.main(exit = False)			