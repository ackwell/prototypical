package ast

import (
	"github.com/ackwell/prototypical/object"
)

type Evaluable interface {
	evaluate(scope object.Context) object.Object
}

type Assignable interface {
	assign(obj object.Object, scope object.Context)
}

type LocationSegment interface {
	Evaluable
	Assignable

	lookup(scope object.Context) object.Context
}
