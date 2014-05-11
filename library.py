
import functools

def definition(function):
	class wrapper:
		def __init__(self):
			self._vars = {}

		@functools.wraps(function)
		def call(self, *args, **kwargs):
			self._vars['result'] = function(*args, **kwargs)
			return self

		def get(self, name):
			if name in self._vars:
				return self._vars[name]

		def set(self, name, value):
			self._vars[name] = value

	return wrapper()

class Library(object):
	def get(self, name):
		name = '_func_' + name
		if hasattr(self, name):
			return getattr(self, name)

	@definition
	def _func_in(args):
		print(*args, end='', flush=True)
		return input()

	@definition
	def _func_out(args):
		print(*args)

	def set(self, name, value):
		raise SyntaxError() # TODO: more info, can't have them overriding builtins
