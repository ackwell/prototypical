package parser

import (
	"io/ioutil"
	"github.com/ackwell/prototypical/token"
)

func ParseFile(filename string) {
	source, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}

	var p parser
	p.init(source)

	_ = p.parseBody(token.EOF)
}
