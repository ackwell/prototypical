
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
		"assign = location, ('=' | compound_assignment), formula;"
		if location is None:
			location = self._parse_location()

		assign = nodes.Assign(location=location)

		# Translate compound assignments into standard assignments
		op = None
		if self._peek() == 'compound assignment':
			# Get the operation
			op = self._token.val.strip('=')

		# Should be an assignment, throw hissy
		elif self._peek() != '=':
			...

		# Eat assignment operator
		self._next()

		# Grab the formula, and create compound if needed
		formula = self._parse_formula()
		if op:
			formula = nodes.Operation(op, location, formula)

		assign.formula = formula

		return assign

	def _parse_formula(self):
		"formula = value, {operation, value};"
		first = self._parse_value()
		return self._parse_formula_precedence(first)

	def _parse_formula_precedence(self, left, last_prec=0):
		# Precedence based parsing
		while True:
			op = self._peek()

			prec = self._get_precedence(op)
			if prec < last_prec:
				return left

			self._next()

			right = self._parse_value()

			next_prec = self._get_precedence(self._peek())
			if prec < next_prec:
				right = self._parse_formula_precedence(right, prec + 1)

			left = nodes.Operation(op, left, right)

		return left

	def _parse_value(self):
		"""
		value = number
		        | string
		        | group
		        | location
		        | call
		        | definition;
		"""
		key = self._peek()

		# Number
		if key == 'number':
			node = nodes.Literal(float(self._token.val))
			self._next()
			return node

		# String
		if key == 'string':
			...

		# Grouping: delegate because this gon be ugly
		if key == '(':
			return self._parse_paren()

		raise SyntaxError

	def _parse_paren(self):
		self._next()
		pos = self._token.pos

		# Find the first token after closing paren
		self.nested = 1
		while self.nested > 0:
			key = self._peek()
			if key == '(':
				self.nested += 1
			elif key == ')':
				self.nested -= 1
			self._next()

		# Check if it's a function body
		if self._peek() == '{':
			... # TODO: Parse function body

		else:
			self._lexer.jump(pos)
			self._next()
			formula = self._parse_formula()
			self._next()
			return formula

	def _get_precedence(self, op):
		return self._precedence[op] if op in self._precedence else -1

	def _peek(self):
		return self._token.key

	def _next(self):
		self._token = self._lexer.next()
