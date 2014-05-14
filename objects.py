# Core
class Body(object):
	def __init__(self, expressions=None, parents=None):
		if expressions is None:
			expressions = []
		if parents is None:
			parents = []

		self._items = expressions
		self._parents = parents
		self._context = {}

	def add_parent(self, parent):
		self._parents.append(parent)

	def call(self, arguments=None):
		# Arguments (if passed) will be {name: value} that should be added to context
		if arguments:
			self._context.update(arguments)

		for expression in self._items:
			expression.execute(self)
		return self

	def get(self, name, limiter=''):
		if 'self' in limiter:
			if name in self._context:
				return self._context[name]

		if 'parent' in limiter:
			for parent in self._parents:
				result = parent.get(name, limiter)
				if result:
					return result

		# Nothing found, null it
		return Null()

	def set(self, name, value, limiter=''):
		# Check local scope first
		if 'self' in limiter and name in self._context:
			self._context[name] = value
			return

		# Wasn't local, check parents
		if 'parent' in limiter:
			for parent in self._parents:
				if parent.get(name, limiter):
					parent.set(name, value, limiter)
					return

		# Wasn't in a parent either, set new var locally
		if 'self' in limiter:
			self._context[name] = value
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