package object

import (
	"github.com/ackwell/prototypical/ast"
)

type Object interface {

}

type Function struct {
	expressions []ast.Expression

	parents []*Context
	defaults map[string]*Object
}

func NewFunction(expressions []ast.Expression) *Function {
	function := new(Function)

	function.expressions = expressions

	return function
}

func (f *Function) call() {

}

type Context struct {}
