
from lexer import Lexer
import nodes

class Parser(object):
	def __init__(self, filename):
		self._lexer = Lexer(filename)
		# Advance to first token
		self._next()

	def parse(self):
		# The body of a document is treated as a function
		return self._parse_body('eof')

	def _parse_body(self, end='}'):
		"body = {expression};"
		body = nodes.Body()
		# Capture expressions until we reach end
		while self._peek() != end:
			body.add(self._parse_expression())
		return body

	def _parse_expression(self):
		"expression = (assignment | function_call), ';';"
		location = self._parse_location()

		# Next token is '(', it's a function call
		if self._peek() == '(':
			...

		# Otherwise, it's an assignment
		return self._parse_assign(location)

	def _parse_location(self):
		"location = [clone, '.'], identifier, {'.', identifier};"
		location = nodes.Location()

		# If first token is '|', parse the clone first
		if self._peek() == '|':
			...

		# TODO: Error handle when no iden

		while True:
			location.add(nodes.Identity(self._token.val))
			# If next token isn't '.', break out
			self._next()
			if self._peek() != '.':
				break
			# Consume the '.'
			self._next()

		return location

	def _parse_assign(self, location = None):
		if location == None:
			location = self._parse_location()

		...

	def _peek(self):
		return self._token.key

	def _next(self):
		self._token = self._lexer.next()
