# Core
class Function(object):
	def __init__(self, expressions, parameters=None):
		if parameters is None:
			parameters = []

		self._expressions = expressions
		self._parameters = parameters
		self._parents = []

	def add_parent(self, parent):
		self._parents.append(parent)

	def call(self, arguments=None, scope=None):
		if arguments is None:
			arguments = []

		arg_map = dict(zip(map(lambda i: i.name, self._parameters), arguments))

		parents = list(self._parents)
		if scope:
			parents.append(Namespace('scope', scope))

		context = Context(arg_map, parents)

		for expression in self._expressions:
			expression.execute(context)
		return context
	__call__ = call

# Special context used to limit values to a namespace
class Namespace(object):
	def __init__(self, name, value):
		self._name = name
		self._value = value

	def get(self, name, limiter=''):
		if name == self._name:
			return self._child
		return Null()

	def set(self, name, value, limiter=''):
		# Can't override a namespace, soz
		raise AttributeError() # TODO: more info

class Context(object):
	def __init__(self, values=None, parents=None):
		if values is None:
			values = {}
		if parents is None:
			parents = []

		self._values = values
		self._parents = parents

	def get(self, name, limiter=''):
		if 'self' in limiter:
			if name in self._values:
				return self._values[name]

		if 'parent' in limiter:
			for parent in self._parents:
				result = parent.get(name, limiter)
				if result:
					return result

		# Nothing found, null it
		return Null()

	def set(self, name, value, limiter=''):
		# Check local scope first
		if 'self' in limiter and name in self._values:
			self._values[name] = value
			return

		# Wasn't local, check parents
		if 'parent' in limiter:
			for parent in self._parents:
				if parent.get(name, limiter):
					parent.set(name, value, limiter)
					return

		# Wasn't in a parent either, set new var locally
		if 'self' in limiter:
			self._values[name] = value
			return

		# Limiter excluding self, but nothing found. Raise error.
		raise AttributeError() # TODO: more info


# Acts as a context, and value. Absorbs all sets and returns itself when retrieved.
class Null(object):
	def evaluate(self, scope):
		return self

	def assign(self, value, scope):
		pass

	def get(self, name, limiter=''):
		return self

	def set(self, name, value, limiter=''):
		pass

	def string(self, indent=0):
		return  ' '*indent+'(null)';

	def __bool__(self):
		return False