# Core
class Function(object):
	def __init__(self, expressions, parameters=None):
		if parameters is None:
			parameters = []

		self._expressions = expressions
		self._parameters = parameters
		self._parents = []
		self._defaults = {}

	def add_parent(self, parent):
		self._parents.append(parent)

	def add_defaults(self, defaults):
		self._defaults.update(defaults)

	def call(self, arguments=None, scope=None, context=None):
		if arguments is None:
			arguments = []

		# Seperate function so that children may use.
		if context is None:
			context = self.initiate_context(arguments, scope)

		for expression in self._expressions:
			expression.execute(context)
		return context
	__call__ = call

	def initiate_context(self, arguments=None, scope=None):
		# Copy, so as to avoid tainting the defaults for next call
		defaults = self._defaults.copy()
		if arguments is not None:
			arg_map = dict(zip(map(lambda i: i.name, self._parameters), arguments))
			defaults.update(arg_map)

		parents = list(self._parents)
		if scope is not None:
			parents.append(Namespace('scope', scope))

		return Context(defaults, parents)

# Special context used to limit values to a namespace
class Namespace(object):
	def __init__(self, name, value):
		self._name = name
		self._value = value

	def get(self, name, limiter=''):
		if name == self._name:
			return self._value
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

	def get(self, name, limiter='self'):
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

	def set(self, name, value, limiter='self'):
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