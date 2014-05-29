package object

type Object interface {
}

type Expression interface {
	Execute(scope *Context)
}

type Function struct {
	expressions []Expression
	parameters  []string

	parents  []*Context
	defaults map[string]*Object
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
	return nil
}

func (f *Function) CallWithContext(context *Context) *Context {
	for _, expression := range f.expressions {
		expression.Execute(context)
	}

	return context
}

type Context struct{}
