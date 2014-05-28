package parser

import (
	"io/ioutil"
	"github.com/ackwell/prototypical/token"
	"github.com/ackwell/prototypical/object"
)

func ParseFile(filename string) *object.Function {
	source, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	var p parser
	p.init(source)

	return object.NewFunction(p.parseBody(token.EOF))
}
