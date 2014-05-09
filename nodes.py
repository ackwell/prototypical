
# Base Classes
class Node(object):
	def __str__(self):
		return self.string()

	# def string(self, indent = 0):
	# 	raise NotImplementedError()

class Expression(Node):
	def evaluate(self):
		raise NotImplementedError()

class Group(Node):
	def __init__(self, items=None):
		if items is None: items = []
		self._items = items

	def add(self, item):
		self._items.append(item)

	def string(self, indent=0):
		string = [' ' * indent, '(', self.__class__.__name__.lower(), '\n']
		for item in self._items:
			string.append(item.string(indent + 1))
		string += [' ' * indent, ')\n']
		return ''.join(string)

# Core
class Body(Group):
	pass

# Location
class Location(Group):
	pass

class Identity(Node):
	def __init__(self, name=''):
		self.name = name

	def string(self, indent = 0):
		return "{}(identity '{}')\n".format(' ' * indent, self.name)

# Expressions
class Assign(Expression):
	def __init__(self, location=None, formula=None):
		self.location = location
		self.formula = formula

	def string(self, indent = 0):
		string = [' ' * indent, '(assign\n',
			self.location.string(indent + 1),
			self.formula.string(indent + 1),
			' ' * indent, ')\n'
		]
		return ''.join(string)

class Call(Expression):
	...

# Operations
class Operation(Node):
	def __init__(self, op='', left=None, right=None):
		self.op = op
		self.left = left
		self.right = right

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

	def string(self, indent=0):
		return "{}(literal '{}')\n".format(' ' * indent, self.value)
