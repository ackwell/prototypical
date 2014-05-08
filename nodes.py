
# Base Classes
class Node(object):
	def __str__(self):
		return self.string()

	def string(self, indent = 0):
		raise NotImplementedError()

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
	def __init__(self, location=None, value=None):
		self.location = location
		self.value = value

	def string(self, indent = 0):
		string = [' ' * indent, '(assign\n',
			self.location.string(indent + 1),
			# self.value.string(),
			' ' * indent, ')\n'
		]

		return ''.join(string)

class Call(Expression):
	...

# Literals
# TODO: Look into making literals into objects (in representation)
class Literal(Node):
	def __init__(self, value=None):
		self.value = value
