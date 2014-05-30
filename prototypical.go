package main

import (
	"github.com/ackwell/prototypical/parser"
	"github.com/ackwell/prototypical/object"
	"github.com/davecgh/go-spew/spew"
)

func main() {
	// Somewhat temp, will need to modify to add stdlib
	arguments := make([]object.Object, 0)
	scope := &object.Dictionary{make(map[string]object.Object), make([]object.Context, 0)}

	rootFunction := parser.ParseFile("test.prt")
	thing := rootFunction.Call(arguments, scope)
	spew.Dump(thing)
}
