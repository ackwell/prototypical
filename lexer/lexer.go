// Heavily borrows from package go/scanner.
// All rights for derivative work go to original authors and all that.

package lexer

import (
	"github.com/ackwell/prototypical/token"
	"unicode"
	"unicode/utf8"
)

type Lexer struct {
	src []byte

	char            rune
	pos             int
	readPos         int
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
nextToken:
	l.ignoreWhitespace()

	pos = l.pos
	insertSemicolon := false

	switch char := l.char; {
	// Identifier or keyword
	case isLetter(char):
		lit = l.checkIdentifier()
		tok = token.Lookup(lit)
		insertSemicolon = true

	case isDigit(char):
		lit = l.checkNumber(false)
		tok = token.NUMBER
		insertSemicolon = true

	default:
		l.next()
		switch char {
		// Comment
		case '#':
			l.consumeComment()
			goto nextToken

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

		case '\'', '"':
			tok = token.STRING
			lit = l.checkString(char)
			insertSemicolon = true

		// Operators and compound assignments, and the insert token
		case '+':
			tok = l.switchToken(token.ADD, '=', token.ADD_EQUALS)
		case '-':
			tok = l.switchToken(-1, '=', token.SUBTRACT_EQUALS)
			if tok == -1 {
				tok = l.switchToken(token.SUBTRACT, '>', token.INSERTION)
			}
		case '*':
			tok = l.switchToken(token.MULTIPLY, '=', token.MULTIPLY_EQUALS)
		case '/':
			tok = l.switchToken(token.DIVIDE, '=', token.DIVIDE_EQUALS)
		case '%':
			tok = l.switchToken(token.MODULUS, '=', token.MODULUS_EQUALS)

		// Comparisons
		case '>':
			tok = l.switchToken(token.GREATER, '=', token.GREATER_EQUAL)
		case '<':
			tok = l.switchToken(token.LESS, '=', token.LESS_EQUAL)
		case '!':
			tok = l.switchToken(token.NOT, '=', token.NOT_EQUAL)
		// Possibly handle binary ops later (& and |)
		case '&':
			tok = l.switchToken(token.UNKNOWN, '&', token.AND)
		case '|':
			tok = l.switchToken(token.PIPE, '|', token.OR)
			if tok == token.PIPE {
				insertSemicolon = true
			}

		// Punctuation
		case '=':
			tok = token.EQUALS
		case '.':
			if isDigit(l.char) {
				lit = l.checkNumber(true)
				tok = token.NUMBER
				insertSemicolon = true
			} else {
				tok = token.PERIOD
			}
		case ',':
			tok = token.COMMA
		case ';':
			tok = token.SEMICOLON
			lit = ";"

		case '(':
			tok = token.PAREN_LEFT
		case ')':
			tok = token.PAREN_RIGHT
			insertSemicolon = true
		case '{':
			tok = token.BRACE_LEFT
		case '}':
			tok = token.BRACE_RIGHT
			insertSemicolon = true
		case '[':
			tok = token.BRACKET_LEFT
		case ']':
			tok = token.BRACKET_RIGHT
			insertSemicolon = true
		}
	}

	l.insertSemicolon = insertSemicolon

	if tok == token.UNKNOWN {
		lit = string(l.char)
	}

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

func (l *Lexer) consumeComment() {
	for l.char != '\n' {
		l.next()
	}
	l.next()
}

func (l *Lexer) checkIdentifier() string {
	start := l.pos

	for isLetter(l.char) || isDigit(l.char) {
		l.next()
	}

	return string(l.src[start:l.pos])
}

func (l *Lexer) checkNumber(seenPeriod bool) string {
	start := l.pos
	pointConsumed := false

	if seenPeriod {
		start -= 1
		pointConsumed = true
	}

	for isDigit(l.char) || l.char == '.' {
		// Only consume one point
		if l.char == '.' {
			if pointConsumed {
				break
			}
			pointConsumed = true
		}

		l.next()
	}

	return string(l.src[start:l.pos])
}

func (l *Lexer) checkString(quote rune) string {
	start := l.pos - 1

	for l.char != quote {
		char := l.char
		l.next()
		if char == '\n' || char < 0 {
			l.error("String not terminated")
			break
		}
		// TODO: handle escapes
	}

	l.next()
	return string(l.src[start:l.pos])
}

func (l *Lexer) switchToken(tok1 token.Token, char2 rune, tok2 token.Token) token.Token {
	if l.char == char2 {
		l.next()
		return tok2
	}
	return tok1
}

// Byte order mark
const byteOrderMark = 0xFEFF

func (l *Lexer) next() {
	if l.readPos >= len(l.src) {
		// char < 0 == EOF
		l.char = -1
		l.pos = len(l.src)
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

func isLetter(char rune) bool {
	return 'a' <= char && char <= 'z' || 'A' <= char && char <= 'Z' || char == '_' || char >= 0x80 && unicode.IsLetter(char)
}

func isDigit(char rune) bool {
	return '0' <= char && char <= '9' || char >= 0x80 && unicode.IsDigit(char)
}
