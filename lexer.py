
class Token(object):
	def __init__(self, pos, key, val):
		self.pos, self.key, self.val = pos, key, val

class Lexer(object):
	def __init__(self, filename):
		f = open(filename, 'r', encoding='utf-8')
		self._source = f.read()

		self._pos = 0
		self._length = len(self._source)
		self._last = Token(None, None, None)

		self._checks = [
			'eof',
			'whitespace',
			'comments',
			'string',
			'number',
			'compound',
			'punctuation',
			'identifier',
			'unknown'
		]

		self._compound = {
			'comparison': {
				'first':  ['<', '>', '!', '='],
				'second': ['='],
				'single': ['<', '>']
			},
			'compound assignment': {
				'first':  ['+', '-', '*', '/'],
				'second': ['='],
				'single': []
			},
			'insert': {
				'first':  ['-'],
				'second': ['>'],
				'single': []
			}
		}

		self._punctuation = [
			'.',
			'(', ')',
			'{', '}',
			'@', '^',
			'+', '-', '*', '/',
			'='
		]

		self._keywords = [
			'if',
			'else',
			'for',
			'while'
		]

	# So that the caller can rewind/fast forward to a position
	def jump(self, pos):
		self._pos = pos

	def next(self):
		for check in self._checks:
			result = getattr(self, '_check_' + check)()
			if result != None:
				self._last = result
				return result

	def _check_eof(self):
		if self._peek() == None:
			return Token(self._pos, 'eof', 'eof')

	def _check_whitespace(self):
		# If there's already a newline token, we can skip multiple blank lines
		# if self._last.key == 'newline':
		self._get_while(lambda c: c.isspace())

		# Keep a newline token
		# else:
		# 	self._get_while(lambda c: c != '\n' and c.isspace())
		# 	if self._peek() == '\n':
		# 		self._next()
		# 		return Token(self._pos - 1, 'newline', '\n')

	def _check_comments(self):
		# Ignore comments
		if self._peek() == '#':
			self._get_while(lambda c: c != '\n')
			return self.next()

	def _check_string(self):
		char = self._peek()
		if char in '\'"':
			quote, pos = char, self._pos
			self._next()
			string = self._get_while(lambda c: c != quote)
			self._next()
			return Token(pos, 'string', string)

	def _check_number(self):
		if self._peek().isdigit():
			pos = self._pos
			number = self._get_while(lambda c: c.isdigit())
			return Token(pos, 'number', number)

	def _check_compound(self):
		first = self._peek()
		for token, options in self._compound.items():
			if first not in options['first']:
				continue
			pos = self._pos
			self._next()
			second = self._peek()
			if second in options['second']:
				self._next()
				return Token(pos, token, first + second)
			if first in options['single']:
				return Token(pos, token, first)
			self._prev()

	def _check_punctuation(self):
		char = self._peek()
		if char in self._punctuation:
			self._next()
			return Token(self._pos - 1, char, char)

	def _check_identifier(self):
		char = self._peek()
		if char == '_' or char.isalpha():
			pos = self._pos
			identifier = self._get_while(lambda c: c == '_' or c.isalnum())
			if identifier in self._keywords:
				return Token(pos, identifier, identifier)
			return Token(pos, 'identifier', identifier)

	def _check_unknown(self):
		char = self._peek()
		self._next()
		return Token(self._pos - 1, 'unknown', char)

	def _peek(self):
		if self._pos >= self._length:
			return None
		return self._source[self._pos]

	def _next(self):
		self._pos += 1

	def _prev(self):
		self._pos -= 1

	def _get_while(self, end_func):
		staging = ''
		char = self._peek()
		while end_func(char):
			staging += char
			self._next()
			char = self._peek()
		return staging
