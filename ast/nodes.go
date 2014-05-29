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

func (l *Location) assign(obj object.Object, scope *object.Context) {
	fmt.Println(obj, scope)
}

// Clone
type Clone struct {
	Location *Location
}

// Identity
type Identity struct {
	Name string
}

// Call

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
	return nil
}
