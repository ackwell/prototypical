
import copy
import operator
import objects

# Base Classes
class Node(object):
	def __str__(self):
		return self.string()

	# def _string(self, indent = 0):
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

# Seriously hacky shit used by other nodes to fake scopes
class Namespace(object):
	def __init__(self, name, child):
		self._name = name
		self._child = child

	def get(self, name, limiter=''):
		if name == self._name:
			return self._child
		return Null()

	def set(self, name, value, limiter=''):
		# Can't override a namespace, soz
		raise AttributeError() # TODO: more info

# Location
class Location(Group):
	def execute(self, scope):
		return self.evaluate(scope)

	def evaluate(self, scope):
		scope = self._lookup_parent(scope)
		return self._items[-1].evaluate(scope)

	def assign(self, value, scope):
		scope = self._lookup_parent(scope)
		self._items[-1].assign(value, scope)

	def _lookup_parent(self, scope):
		for identity in self._items[:-1]:
			scope = identity.evaluate(scope)
			if scope == None:
				return Null()
		return scope

class Clone(Location):
	def __init__(self, location=None):
		self.location = location

	def evaluate(self, scope):
		return copy.deepcopy(self.location.evaluate(scope))

	def assign(self, value, scope):
		# Setting on a clone serves no purpose.
		# TODO: throw error?
		...

	def string(self, indent=0):
		string = [' ' * indent, '(clone\n',
			self.location.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

# Idenities (inc. calls)
class Identity(Node):
	def __init__(self, name=''):
		self.name = name
		self.limiters = {
			'@': 'self',
			'^': 'parent',
			'default': 'self parent'
		}

	def evaluate(self, scope):
		name, limiter = self._find_limiter()
		return scope.get(name, limiter)

	def assign(self, value, scope):
		name, limiter = self._find_limiter()
		return scope.set(name, value, limiter)

	def _find_limiter(self):
		prefix = self.name[0]
		if prefix in self.limiters:
			return self.name[1:], self.limiters[prefix]
		return self.name, self.limiters['default']

	def string(self, indent=0):
		return "{}(identity '{}')\n".format(' ' * indent, self.name)

class Call(Group):
	def __init__(self, location=None, arguments=None):
		super().__init__(arguments)
		self.location = location

	def evaluate(self, scope):
		# Evaluate the arguments
		arguments = list(map(lambda i: i.evaluate(scope), self._items))

		# Get the function, add the calling scope as 'chain', and call it
		function = self.location.evaluate(scope)
		return function.call(arguments)

	def string(self, indent=0):
		string = [' ' * indent, '(call\n',
			self.location.string(indent + 1),
			self._string_items(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

# Expressions
class Assign(Node):
	def __init__(self, location=None, formula=None):
		self.location = location
		self.formula = formula

	def execute(self, scope):
		# Need to have scope, so let python chuck a hissy if none is passed
		result = self.formula.evaluate(scope)
		self.location.assign(result, scope)

	def string(self, indent=0):
		string = [' ' * indent, '(assign\n',
			self.location.string(indent + 1),
			self.formula.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

class Definition(Group):
	def __init__(self, parameters=None, body=None):
		super().__init__(parameters)
		self.body = body

		self._parents = []

	def add_parent(self, parent):
		self._parents.append(parent)

	def evaluate(self, scope):
		# Not being run, just assigned. The scope passed is that of the parent,
		# so add it to the body
		self._parents.append(scope)
		return self

	def call(self, arguments):
		# This time, it's actually being called. Map args and pass to body
		# TODO: Default args, possible named params
		if len(arguments) != len(self._items):
			raise TypeError() # TODO: More info

		arguments = dict(zip(map(lambda i: i.name, self._items), arguments))
		func = objects.Body(self.body, self._parents)
		return func.call(arguments)
	__call__ = call

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

		self.ops = {
			'+':  operator.add,
			'-':  operator.sub,
			'*':  operator.mul,
			'/':  operator.truediv,
			'%':  operator.mod,
			'<':  operator.lt,
			'<=': operator.le,
			'>':  operator.gt,
			'>=': operator.ge,
			'==': operator.eq,
			'!=': operator.ne
		}

	def evaluate(self, scope):
		# Probably expand to do something else or some shit i dunno
		left, right = self.left.evaluate(scope), self.right.evaluate(scope)

		if self.op in self.ops:
			return self.ops[self.op](left, right)

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
