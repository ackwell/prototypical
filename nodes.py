
# Base Classes
class Node(object):
	def __str__(self):
		return self.string()

	# def string(self, indent = 0):
	# 	raise NotImplementedError()

class Group(Node):
	def __init__(self, items=None):
		if items is None: items = []
		self._items = items

	def add(self, item):
		self._items.append(item)

	def string(self, indent=0):
		string = [' ' * indent, '(', self.__class__.__name__.lower(), '\n']
		string.append(self._string_items(indent + 1))
		string += [' ' * indent, ')\n']
		return ''.join(string)

	def _string_items(self, indent=0):
		string = []
		for item in self._items:
			string.append(item.string(indent))
		return ''.join(string)

# Core
class Body(Group):
	def __init__(self, expressions=None):
		super().__init__(expressions)

		self._parents = []
		self._context = {}

	def add_parent(self, parent):
		self._parents.append(parent)

	def evaluate(self, arguments=None):
		# Arguments (if passed) will be {name: value} that should be added to context
		if arguments:
			self._context.update(arguments)

		for expression in self._items:
			expression.evaluate(self)
		return self
	__call__ = evaluate

	def get(self, name):
		if name in self._context:
			return self._context[name]

		for parent in self._parents:
			result = parent.get(name)
			if result:
				return result

	def set(self, name, value):
		# Check local scope first
		if name in self._context:
			self._context[name] = value
			return

		# Wasn't local, check parents
		for parent in self._parents:
			if parent.get(name):
				parent.set(name)
				return

		# Wasn't in a parent either, set new var locally
		self._context[name] = value

# Location
class Location(Group):
	def evaluate(self, scope):
		# Needed so it can be treated as a value
		return self.get(scope)

	def get(self, scope):
		parent = self._lookup_parent(scope)
		return parent.get(self._items[-1].name)

	def set(self, value, scope):
		parent = self._lookup_parent(scope)
		parent.set(self._items[-1].name, value)

	def _lookup_parent(self, scope):
		# Both get/set should fail if more than the last iden does not exist
		for identity in self._items[:-1]:
			scope = identity.evaluate(scope)
			if scope == None:
				raise AttributeError() # TODO: Expand with more info
		return scope

class Identity(Node):
	def __init__(self, name=''):
		self.name = name

	def evaluate(self, scope):
		return scope.get(self.name)

	def string(self, indent=0):
		return "{}(identity '{}')\n".format(' ' * indent, self.name)

# Expressions
class Assign(Node):
	def __init__(self, location=None, formula=None):
		self.location = location
		self.formula = formula

	def evaluate(self, scope):
		# Need to have scope, so let python chuck a hissy if none is passed
		result = self.formula.evaluate(scope)
		self.location.set(result, scope)

	def string(self, indent=0):
		string = [' ' * indent, '(assign\n',
			self.location.string(indent + 1),
			self.formula.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

class Call(Group):
	def __init__(self, location=None, arguments=None):
		super().__init__(arguments)
		self.location = location

	def evaluate(self, scope):
		# Evaluate the arguments
		arguments = list(map(lambda i: i.evaluate(scope), self._items))

		# Get the function and call it
		function = self.location.get(scope)
		return function.call(arguments)

	def string(self, indent=0):
		string = [' ' * indent, '(call\n',
			self.location.string(indent + 1),
			self._string_items(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

class Definition(Group):
	def __init__(self, parameters=None, body=None):
		super().__init__(parameters)
		self.body = body

	def evaluate(self, scope):
		# Not being run, just assigned. The scope passed is that of the parent,
		# so add it to the body
		self.body.add_parent(scope)
		return self

	def call(self, arguments):
		# This time, it's actually being called. Map args and pass to body
		# TODO: Default args, possible named params
		if len(arguments) != len(self._items):
			raise TypeError() # TODO: More info

		arguments = dict(zip(map(lambda i: i.name, self._items), arguments))
		return self.body.evaluate(arguments)

	def string(self, indent=0):
		string = [' ' * indent, '(definition\n',
			self._string_items(indent + 1),
			self.body.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

# Operations
class Operation(Node):
	def __init__(self, op='', left=None, right=None):
		self.op = op
		self.left = left
		self.right = right

	def evaluate(self, scope):
		# Probably expand to do something else or some shit i dunno
		left, right = self.left.evaluate(scope), self.right.evaluate(scope)

		if self.op == '+':
			return left + right
		elif self.op == '-':
			return left - right
		elif self.op == '*':
			return left * right
		elif self.op == '/':
			return left / right

	def string(self, indent=0):
		string = [' ' * indent, '(operation ', self.op, '\n',
			self.left.string(indent + 1),
			self.right.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

# Literals
# TODO: Look into making literals into objects (in representation)
class Literal(Node):
	def __init__(self, value=None):
		self.value = value

	def evaluate(self, scope):
		return self.value

	def string(self, indent=0):
		return "{}(literal '{}')\n".format(' ' * indent, self.value)
