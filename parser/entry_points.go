package parser

import (
	"github.com/ackwell/prototypical/object"
	"github.com/ackwell/prototypical/token"
	"io/ioutil"
)

func ParseFile(filename string) *object.Function {
	source, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	var p parser
	p.init(source)

	params := make([]string, 0);
	return object.NewFunction(params, p.parseBody(token.EOF))
}
