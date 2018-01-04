class test_class:
	"""docstring for test_class"""
	adress = ''
	def __init__(self, *argv):
		if argv:
			self.adress = argv[0]
		else:
			print('no adress')