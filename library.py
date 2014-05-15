
import functools
import objects

def definition(function):
	class wrapper(objects.Function):
		@functools.wraps(function)
		def call(self, args, scope):
			# Args are going to be passed directly to function, so ignore from context
			context = self.initiate_context([], scope)
			result = function(context, *args)
			context.set('result', result)
			return context
	return wrapper([])

class Library(object):
	def get_context(self):
		context = {}
		for name, func in self.functions():
			context[name] = func
		return context

	def set_parents(self, parent):
		for _, func in self.functions():
			func.add_parent(parent)

	def functions(self):
		for member in dir(self):
			if member.startswith('_func_'):
				yield member[6:], getattr(self, member)

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
		test = func.get('scope', 'parent').get('result', 'self parent')
		if test:
			# Previous chain has was truthy, so cop out here
			return
		callback.call([]);
