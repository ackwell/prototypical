package object

// Only really here to prevent recursive import
type Expression interface {
	Execute(scope Context)
}

// All object interfaces need to include Object so I can throw around values
type Object interface {
	Type() string
}

type Context interface {
	Object
	
	Get(name string) Object
	Set(name string, value Object)
}
