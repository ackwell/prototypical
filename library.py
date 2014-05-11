
import functools

def definition(function):
	class wrapper:
		@functools.wraps(function)
		def call(*args, **kwargs):
			function(*args, **kwargs)
	return wrapper

class Library(object):
	def get(self, name):
		name = '_func_' + name
		if hasattr(self, name):
			return getattr(self, name)

	@definition
	def _func_out(args):
		print(*args)	

	def set(self, name, value):
		raise SyntaxError() # TODO: more info, can't have them overriding builtins
