package main

import (
	"fmt"
	"github.com/ackwell/prototypical/lexer"
	"github.com/ackwell/prototypical/token"
	"io/ioutil"
)

func main() {
	source, err := ioutil.ReadFile("test.prt")
	if err != nil {
		panic(err)
	}

	// Temp: lexing manually
	l := lexer.New(source)
	for {
		pos, tok, lit := l.Next()
		fmt.Println(pos, tok, lit)
		if tok == token.EOF {
			break
		}
	}
}
