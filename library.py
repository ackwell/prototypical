
import functools
import objects

def definition(function):
	# Actually takes the place of a Function object as well, but
	# this handles all of that extra stuff anyway.
	class wrapper(objects.Body):
		@functools.wraps(function)
		def call(self, args):
			self._context['result'] = function(self, *args)
			return self

		def __str__(self):
			return str(function)

	# TODO: perhaps wrap further to gen new body objects on the fly
	return wrapper()

class Library(object):
	def get_context(self, scope):
		context = {}
		for member in dir(self):
			if member.startswith('_func_'):
				func = getattr(self, member)
				func.add_parent(scope)
				context[member[6:]] = func
		return context

	@definition
	def _func_in(func, *args):
		print(*args, end='', flush=True)
		return input()

	@definition
	def _func_out(func, *args):
		print(*args)

	@definition
	def _func_if(func, condition, callback):
		if condition:
			callback.call([])
		return condition

	@definition
	def _func_else(func, callback):
		if func.get('scope', 'parent').get('result', 'self parent'):
			# Previous chain has was truthy, so cop out here
			return
		callback.call([]);
