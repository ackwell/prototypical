
from lexer import Lexer

class Parser(object):
	def __init__(self, filename):
		self.lexer = Lexer(filename)

	def parse(self):
		...
