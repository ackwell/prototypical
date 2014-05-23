package main

import (
	"github.com/ackwell/prototypical/lexer"
	"io/ioutil"
	"fmt"
)

func main() {
	source, err := ioutil.ReadFile("test.prt")
	if err != nil {
		panic(err)
	}

	// Temp: lexing manually
	lexer := lexer.New(source)
	fmt.Println(lexer.Next())
}
