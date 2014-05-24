package lexer

import (
	"unicode"
	"github.com/ackwell/prototypical/token"
	"unicode/utf8"
)

type Lexer struct {
	src []byte

	char rune
	pos int
	readPos int
	insertSemicolon bool
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
	l.readPos = 0
	l.insertSemicolon = false
}

func (l *Lexer) Next() (pos int, tok token.Token, lit string) {
// nextToken:
	l.ignoreWhitespace()

	pos = l.pos
	insertSemicolon := false

	switch char := l.char; {
	// Identifier or keyword
	case isLetter(char):
		lit = l.checkIdentifier()
		tok = token.Lookup(lit)
		insertSemicolon = true

	default:
		l.next()
		switch char {
		// EOF
		case -1:
			if l.insertSemicolon {
				l.insertSemicolon = false
				return pos, token.SEMICOLON, "\n"
			}
			tok = token.EOF

		// Newlines here mean we need to insert a semicolon
		case '\n':
			l.insertSemicolon = false
			return pos, token.SEMICOLON, "\n"
		}
	}

	l.insertSemicolon = insertSemicolon

	return
}

func (l *Lexer) ignoreWhitespace() {
	for unicode.IsSpace(l.char) {
		if l.char == '\n' && l.insertSemicolon {
			break
		}
		l.next()
	}
}

func (l *Lexer) checkIdentifier() string {
	start := l.pos

	for isLetter(l.char) || isDigit(l.char) {
		l.next()
	}

	return string(l.src[start:l.pos])
}

// Byte order mark
const byteOrderMark = 0xFEFF

func (l *Lexer) next() {
	if l.readPos >= len(l.src) {
		// char < 0 == EOF
		l.char = -1
		return
	}

	l.pos = l.readPos

	char, width := rune(l.src[l.readPos]), 1
	switch {
	// Disallow NUL
	case char == 0:
		l.error("Invalid character NUL")

	// Handle non-ASCII
	case char >= 0x80:
		char, width = utf8.DecodeRune(l.src[l.readPos:])
		if char == utf8.RuneError && width == 1 {
			l.error("Illegal UTF-8 encoding")
		} else if char == byteOrderMark && l.pos > 0 {
			l.error("Illegal byte order mark")
		}
	}

	l.readPos += width
	l.char = char
}

func (l *Lexer) error(message string) {
	panic(message)
}


// 'Borrowed' from go/scanner.
func isLetter(char rune) bool {
	return 'a' <= char && char <= 'z' || 'A' <= char && char <= 'Z' || char == '_' || char >= 0x80 && unicode.IsLetter(char)
}

func isDigit(char rune) bool {
	return '0' <= char && char <= '9' || char >= 0x80 && unicode.IsDigit(char)
}
