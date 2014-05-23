package lexer

import (
	"unicode"
	"github.com/ackwell/prototypical/token"
)

type Lexer struct {
	src []byte

	char rune
	pos int
}

func New(src []byte) Lexer {
	lexer := Lexer{}
	lexer.Init(src)
	return lexer
}

func (l *Lexer) Init(src []byte) {
	l.src = src

	l.char = ' '
	l.pos = 0
}

func (l *Lexer) Next() (tok token.Token) {
// nextToken:
	return token.UNKNOWN
}

func (l *Lexer) ignoreWhitespace() {
	for isWhitespace(l.char) {
		l.next()
	}
}

func (l *Lexer) next(){

}

func isWhitespace(char rune) bool {
	return char == ' ' || char == '\t' || char == '\n' || char == '\r'
}

// 'Borrowed' from go/scanner.
func isLetter(char rune) bool {
	return 'a' <= char && char <= 'z' || 'A' <= char && char <= 'Z' || char == '_' || char >= 0x80 && unicode.IsLetter(char)
}

func isDigit(char rune) bool {
	return '0' <= char && char <= '9' || char >= 0x80 && unicode.IsDigit(char)
}
