
from lexer import Lexer
import nodes

class Parser(object):
	def __init__(self, filename):
		self._lexer = Lexer(filename)
		# Advance to first token
		self._next()

		self._precedence = {
			'!': 3,
			'*': 2, '/': 2, '%': 2,
			'+': 1, '-': 1
		}

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
		expression = None

		# Next token is '(', it's a function call
		if self._peek() == '(':
			...

		# Otherwise, it's an assignment
		else:
			expression = self._parse_assign(location)

		# TODO: Catch expression is None and peek != ';'
		# Consume ';'
		self._next()
		return expression

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
		"assign = location, ('=' | compound_assignment), value;"
		if location is None:
			location = self._parse_location()

		assign = nodes.Assign(location=location)

		# Translate compound assignments into standard assignments
		if self._peek() == 'compound assignment':
			...

		# Should be an assignment, throw hissy
		elif self._peek() != '=':
			...

		# Eat assignment operator
		self._next()

		assign.value = self._parse_value()

		return assign

	def _parse_value(self):
		"value = element, {operation, element};"
		first = self._parse_element()
		return self._parse_value_precedence(first)

	def _parse_value_precedence(self, left, last_prec=0):
		# Precedence based parsing
		while True:
			op = self._peek()

			prec = self._get_precedence(op)
			if prec < last_prec:
				return left

			self._next()

			right = self._parse_element()

			next_prec = self._get_precedence(self._peek())
			if prec < next_prec:
				right = self._parse_value_precedence(right, prec + 1)

			left = nodes.Operation(op, left, right)

		return left

	def _parse_element(self):
		"""
		element = number
		        | string
		        | location
		        | call
		        | definition;
		"""
		# Number
		if self._peek() == 'number':
			node = nodes.Literal(float(self._token.val))
			self._next()
			return node

		# String
		if self._peek() == 'string':
			...

	def _get_precedence(self, op):
		return self._precedence[op] if op in self._precedence else -1

	def _peek(self):
		return self._token.key

	def _next(self):
		self._token = self._lexer.next()
