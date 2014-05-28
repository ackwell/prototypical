package ast

import (
	"github.com/ackwell/prototypical/token"
)

// Location
type Location struct {
	segments []LocationSegment
}

func (l *Location) AddSegment(segment LocationSegment) {
	l.segments = append(l.segments, segment)
}

func (l *Location) execute() {

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
	Location *Location
	Formula  Evaluable
}

func (a *Assign) execute() {

}

// Insert

// Definition

// Unary
type Unary struct {
	Operator token.Token
	Value    Evaluable
}

func (u *Unary) evaluate() {

}

// Operation
type Operation struct {
	Operation   token.Token
	Left, Right Evaluable
}

func (o *Operation) evaluate() {

}

// Literals
type LiteralNumber struct {
	Value float64
}

func (l *LiteralNumber) evaluate() {

}
