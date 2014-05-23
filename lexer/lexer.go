package lexer

import (
	"bytes"
)

type Lexer struct {
	source []byte

	current *bytes.Buffer
	position int
}

func New(source []byte) Lexer {
	lexer := Lexer{}
	lexer.Init(source)
	return lexer
}

func (l *Lexer) Init(source []byte) {
	l.source = source

	l.current = new(bytes.Buffer)
	l.position = 0
}

func (l *Lexer) Next() string {
	return "hello world"
}

func (l *Lexer) next() {

}
