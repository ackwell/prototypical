package token

var keywords map[string]Token

func init() {
	keywords = map[string]Token{
		"true":  TRUE,
		"false": FALSE,
		"null":  NULL,
	}
}

func Lookup(identity string) Token {
	if token, exists := keywords[identity]; exists {
		return token
	}
	return IDENTIFIER
}

func IsCompound(token Token) bool {
	return compound_begin < token && token < compound_end
}

func IsComparison(token Token) bool {
	return comparison_begin < token && token < comparison_end
}

func IsBoolean(token Token) bool {
	return boolean_begin < token && token < boolean_end
}

func IsUnary(token Token) bool {
	return token == SUBTRACT || token == NOT
}

func GetPrecedence(token Token) (precedence int) {
	switch token {
	case NOT:
		precedence = 4

	case MULTIPLY, DIVIDE, MODULUS:
		precedence = 3

	case ADD, SUBTRACT:
		precedence = 2

	default:
		if IsComparison(token) {
			precedence = 1
		} else if IsBoolean(token) {
			precedence = 0
		} else {
			precedence = -1
		}
	}

	return
}
