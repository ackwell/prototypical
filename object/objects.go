package object

// Function

type Function struct {
	expressions []Expression
	parameters  []string

	parents  []Context
	defaults map[string]Object
}

func NewFunction(parameters []string, expressions []Expression) *Function {
	function := new(Function)

	function.parameters = parameters
	function.expressions = expressions

	return function
}

func (f *Function) Call(arguments []Object, scope Context) Context {
	return f.CallWithContext(f.createContext(arguments, scope))
}

func (f *Function) createContext(arguments []Object, scope Context) Context {
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

	return &Dictionary{defaults, f.parents}
}

func (f *Function) CallWithContext(context Context) Context {
	for _, expression := range f.expressions {
		expression.Execute(context)
	}

	return context
}

func (f *Function) Type() string {
	return "function"
}

// Dictionary

type Dictionary struct {
	values  map[string]Object
	parents []Context
}

func (d *Dictionary) Get(name string) Object {
	// TODO: only if local scope allowed
	if value, ok := d.values[name]; ok {
		return value
	}

	// TODO: only if parent scope allowed
	// TODO: probably need to change the conditional down the line
	for _, parent := range d.parents {
		result := parent.Get(name)
		if result != nil {
			return result
		}
	}

	return new(Null)
}

func (d *Dictionary) Set(name string, value Object) {
	// Check local scope
	// TODO: only if local scope allowed
	if _, ok := d.values[name]; ok {
		d.values[name] = value
	}

	// It wasn't local, check parents
	// TODO: only is parent scope is allowed
	// TODO: probably need to change the conditional down the line
	for _, parent := range d.parents {
		if parent.Get(name) != nil {
			parent.Set(name, value)
			return
		}
	}

	// Wasn't in parent either, set new var locally
	// TODO: only if local scope allowed
	d.values[name] = value

	// TODO: when limiting, if it gets this far, throw error
}

func (d *Dictionary) Type() string {
	return "dictionary"
}

// Namespace

type Namespace struct {
	Name string
	Value Object
}

func (n *Namespace) Get(name string) Object {
	if name == n.Name {
		return n.Value
	}
	return new(Null)
}

func (n *Namespace) Set(name string, value Object) {
	// Should not be able to set on a namespace, throw error
}

func (n *Namespace) Type() string {
	return "namespace"
}

// Null

type Null struct{}

func (n *Null) Get(name string) Object {
	return n
}

func (m *Null) Set(name string, value Object) {
	// Setting a value on null does nothing
}

func (n *Null) Type() string {
	return "null"
}

// Number

type Number struct {
	Value float64
}

func (n *Number) Type() string {
	return "number"
}

// String

type String struct {
	Value string
}

func (s *String) Type() string {
	return "string"
}
