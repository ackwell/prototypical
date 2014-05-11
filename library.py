
class Library(object):
	def get(self, name):
		name = '_func_' + name
		if hasattr(self, name):
			return getattr(self, name)

	class _func_out:
		def call(args):
			print(*args)	

	def set(self, name, value):
		raise SyntaxError() # TODO: more info, can't have them overriding builtins
