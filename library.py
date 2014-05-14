
import functools
import objects

def definition(function):
	# Actually takes the place of a Definition node, but
	# this handles all of that extra stuff anyway.
	class wrapper(objects.Body):
		@functools.wraps(function)
		def call(self, args):
			self._context['result'] = function(self, *args)
			return self

	return wrapper()

class Library(object):
	def get(self, name, limiter=''):
		name = '_func_' + name
		if hasattr(self, name):
			return getattr(self, name)

	def set(self, name, value, limiter):
		raise SyntaxError() # TODO: more info, can't have them overriding builtins

	@definition
	def _func_in(func, *args):
		print(*args, end='', flush=True)
		return input()

	@definition
	def _func_out(func, *args):
		print(*args)
