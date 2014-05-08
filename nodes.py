
# Base Classes
class Node(object):
	pass

class Expression(Node):
	def evaluate(self):
		raise NotImplementedError()

# Core
class Body(Node):
	def __init__(self, expressions = []):
		self._expressions = expressions

	def add(self, expression):
		self._expressions.append(expression)

# Expressions
class Assign(Expression):
	def __init__(self, location = None, value = None):
		self.location = location
		self.value = value

class Call(Expression):
	...
