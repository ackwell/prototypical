package object

type Object interface {
}

type Expression interface {
	Execute(scope *Context)
}

// Function

type Function struct {
	expressions []Expression
	parameters  []string

	parents  []*Context
	defaults map[string]Object
}

func NewFunction(parameters []string, expressions []Expression) *Function {
	function := new(Function)

	function.parameters = parameters
	function.expressions = expressions

	return function
}

func (f *Function) Call(arguments []Object, scope *Context) *Context {
	return f.CallWithContext(f.createContext(arguments, scope))
}

func (f *Function) createContext(arguments []Object, scope *Context) *Context {
	// TODO: Throw error if length of args is != length of params (default args/named params?)

	// Copying, so that injected arguments do not taint next call
	defaults := make(map[string]Object)
	for k, v := range f.defaults {
		defaults[k] = v
	}

	for i, parameter := range f.parameters {
		defaults[parameter] = arguments[i]
	}

	// TODO: Add scope to temporary parents list

	return &Context{defaults, f.parents}
}

func (f *Function) CallWithContext(context *Context) *Context {
	for _, expression := range f.expressions {
		expression.Execute(context)
	}

	return context
}

// Context

type Context struct {
	values  map[string]Object
	parents []*Context
}

func (c *Context) Get(name string) Object {
	// TODO: only if local scope allowed
	if value, ok := c.values[name]; ok {
		return value
	}

	// TODO: only if parent scope allowed
	// TODO: probably need to change the conditional down the line
	for _, parent := range c.parents {
		result := parent.Get(name)
		if result != nil {
			return result
		}
	}

	// TODO: return a null object
	return nil
}

func (c *Context) Set(name string, value Object) {
	// Check local scope
	// TODO: only if local scope allowed
	if _, ok := c.values[name]; ok {
		c.values[name] = value
	}

	// It wasn't local, check parents
	// TODO: only is parent scope is allowed
	// TODO: probably need to change the conditional down the line
	for _, parent := range c.parents {
		if parent.Get(name) != nil {
			parent.Set(name, value)
			return
		}
	}

	// Wasn't in parent either, set new var locally
	// TODO: only if local scope allowed
	c.values[name] = value

	// TODO: when limiting, if it gets this far, throw error
}

// Number

type Number struct {
	Value float64
}


// String

type String struct {
	Value string
}
