package token

type Token int

const (
	UNKNOWN Token = iota
	EOF

	literal_begin
	IDENTIFIER // var
	STRING     // "hello world" 'hello world'
	NUMBER     // 123 456.7
	literal_end

	operator_begin
	ADD       // +
	SUBTRACT  // -
	MULTIPLY  // *
	DIVIDE    // /
	MODULUS   // &
	INSERTION // ->
	operator_end

	compound_begin
	ADD_EQUALS      // +=
	SUBTRACT_EQUALS // -=
	MULTIPLY_EQUALS // *=
	DIVIDE_EQUALS   // /=
	MODULUS_EQUALS  // %=
	compound_end

	comparison_begin
	GREATER       // >
	LESS          // <
	GREATER_EQUAL // >=
	LESS_EQUAL    // <=
	NOT_EQUAL     // !=

	AND // &&
	OR  // ||
	NOT // !
	comparison_end

	punctuation_begin
	PERIOD    // .
	COMMA     // ,
	PIPE      // |
	SEMICOLON // ;

	PAREN_LEFT    // (
	PAREN_RIGHT   // )
	BRACE_LEFT    // {
	BRACE_RIGHT   // }
	BRACKET_LEFT  // [
	BRACKET_RIGHT // ]
	punctuation_end

	keywords_begin
	TRUE  // true
	FALSE // false
	NULL  // null
	keywords_end
)

var keywords map[string]Token

func init() {
	keywords = map[string]Token{
		"true": TRUE,
		"false": FALSE,
		"null": NULL,
	}
}

func Lookup(identity string) Token {
	if token, exists := keywords[identity]; exists {
		return token
	}
	return IDENTIFIER
}
