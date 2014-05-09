
from parser import Parser

def execute(filename):
	# Get file
	f = open(filename, 'r', encoding='utf-8')
	source = f.read()

	# Parse and execute it
	parser = Parser(source)
	root = parser()
	result = root()

	return result
