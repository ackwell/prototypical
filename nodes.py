
# Base Classes
class Node(object):
	pass

class Expression(Node):
	def evaluate(self):
		raise NotImplementedError()

class Group(Node):
	def __init__(self, items=[]):
		self._items = items

	def add(self, item):
		self._items.append(item)

# Core
class Body(Group):
	pass

# Location
class Location(Group):
	pass

class Identity(Node):
	def __init__(self, name=''):
		self.name = name

# Expressions
class Assign(Expression):
	def __init__(self, location=None, value=None):
		self.location = location
		self.value = value

class Call(Expression):
	...
