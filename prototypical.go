package main

import (
	"github.com/ackwell/prototypical/parser"
	"github.com/ackwell/prototypical/object"
)

func main() {
	// Somewhat temp, will need to modify to add stdlib
	arguments := make([]object.Object, 0)
	scope := new(object.Context)

	rootFunction := parser.ParseFile("test.prt")
	rootFunction.Call(arguments, scope)
}
