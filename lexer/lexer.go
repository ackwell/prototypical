package lexer

import (
	"unicode"
	"github.com/ackwell/prototypical/token"
)

type Lexer struct {
	src []byte

	pos int
}

func New(src []byte) Lexer {
	lexer := Lexer{}
	lexer.Init(src)
	return lexer
}

func (l *Lexer) Init(src []byte) {
	l.src = src

	l.pos = 0
}

func (l *Lexer) Next() (tok token.Token) {
	return token.UNKNOWN
}

// 'Borrowed' from go/scanner.
func isLetter(ch rune) bool {
	return 'a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || ch == '_' || ch >= 0x80 && unicode.IsLetter(ch)
}

func isDigit(ch rune) bool {
	return '0' <= ch && ch <= '9' || ch >= 0x80 && unicode.IsDigit(ch)
}
