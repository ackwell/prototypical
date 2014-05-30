package ast

import (
	"fmt"
	"github.com/ackwell/prototypical/object"
	"github.com/ackwell/prototypical/token"
)

// Location

type Location struct {
	segments []LocationSegment
}

func (l *Location) AddSegment(segment LocationSegment) {
	l.segments = append(l.segments, segment)
}

func (l *Location) Execute(scope *object.Context) {

}

func (l *Location) evaluate(scope *object.Context) object.Object {
	return l.segments[len(l.segments)-1].evaluate(l.lookupParent(scope))
}

func (l *Location) assign(value object.Object, scope *object.Context) {
	l.segments[len(l.segments)-1].assign(value, l.lookupParent(scope))
}

func (l *Location) lookupParent(scope *object.Context) *object.Context {
	for _, segment := range l.segments[:len(l.segments)-1] {
		scope = segment.lookup(scope)
		// TODO: check for null
	}
	return scope
}

// Clone

type Clone struct {
	Location *Location
}

func (c *Clone) evaluate(scope *object.Context) object.Object {
	return nil
}

func (c *Clone) assign(value object.Object, scope *object.Context) {
}

func (c *Clone) lookup(scope *object.Context) *object.Context {
	return nil
}

// Identity

type Identity struct {
	Name string
}

func (i *Identity) evaluate(scope *object.Context) object.Object {
	return scope.Get(i.Name)
}

func (i *Identity) assign(value object.Object, scope *object.Context) {
	// TODO: scope with ^ and @ limiters

	scope.Set(i.Name, value)
}

func (i *Identity) lookup(scope *object.Context) *object.Context {
	// TODO: scope with ^ and @ limiters
	// TODO: will probably need to type switch this from .eval
	return nil
}

// Call

type Call struct {
	Segment LocationSegment
	Arguments []Evaluable
}

func (c *Call) evaluate(scope *object.Context) object.Object {
	return c.lookup(scope)
}

func (c *Call) assign(value object.Object, scope *object.Context) {

}

func (c *Call) lookup(scope *object.Context) *object.Context {
	// Evaluate arguments
	arguments := make([]object.Object, 0)
	for _, argument := range c.Arguments {
		arguments = append(arguments, argument.evaluate(scope))
	}

	function := c.Segment.evaluate(scope)
	switch t := function.(type) {
	case *object.Function:
		return t.Call(arguments, scope)
	default:
		// TODO: Need to throw error
		fmt.Println("Unexpected type %T", t)
		return nil
	}
}

// Assign

type Assign struct {
	Location Assignable
	Formula  Evaluable
}

func (a *Assign) Execute(scope *object.Context) {
	a.Location.assign(a.Formula.evaluate(scope), scope)
}

// Insert

// Definition

type Definition struct {
	Parameters []string
	Body []object.Expression
}

func (d *Definition) evaluate(scope *object.Context) object.Object {
	function := object.NewFunction(d.Parameters, d.Body)
	// TODO: Add scope as parent
	return function
}

// Unary

type Unary struct {
	Operator token.Token
	Value    Evaluable
}

func (u *Unary) evaluate(scope *object.Context) object.Object {
	return nil
}

// Operation

type Operation struct {
	Operation   token.Token
	Left, Right Evaluable
}

func (o *Operation) evaluate(scope *object.Context) object.Object {
	return nil
}

// Literals

type LiteralNumber struct {
	Value float64
}

func (l *LiteralNumber) evaluate(scope *object.Context) object.Object {
	return &object.Number{l.Value}
}
