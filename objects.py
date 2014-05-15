# Core

# Function value
class Function(object):
	def __init__(self, body, parameters, parents):
		self.body = body
		self._items = parameters
		self._parents = parents
		self._context = {}

	def call(self, arguments):
		# This time, it's actually being called. Map args and pass to body
		# TODO: Default args, possible named params
		if len(arguments) != len(self._items):
			raise TypeError() # TODO: more info

		arguments = dict(zip(map(lambda i: i.name, self._items), arguments))
		arguments.update(self._context)

		func = self.get_body()
		return func.call(arguments)

	def get_body(self):
		# What am i doing even i don't know any more.
		return Body(self.body, self._parents)

# Seriously hacky shit used by nodes to fake a scope
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

# Object formed by a called function
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

	def add_context(self, context):
		self._context.update(context)

	def call(self, arguments=None):
		# Arguments (if passed) will be {name: value} that should be added to context
		if arguments:
			self._context.update(arguments)

		for expression in self._items:
			expression.execute(self)
		return self
	__call__ = call

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