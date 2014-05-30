package parser

import (
	"fmt"
	"github.com/ackwell/prototypical/ast"
	"github.com/ackwell/prototypical/lexer"
	"github.com/ackwell/prototypical/token"
	"github.com/ackwell/prototypical/object"
	"strconv"
)

type parser struct {
	lexer lexer.Lexer

	pos int
	tok token.Token
	lit string
}

func (p *parser) init(source []byte) {
	p.lexer = lexer.New(source)
	p.next()
}

// body = {expression};
func (p *parser) parseBody(end token.Token) (body []object.Expression) {
	// Capture expressions until reach end token
	for p.tok != end {
		body = append(body, p.parseExpression())
	}

	// Eat the end token
	p.next()

	return body
}

// expression = location, [assign | insert];
func (p *parser) parseExpression() (expression object.Expression) {
	location := p.parseLocation()

	switch {
	case p.tok == token.EQUALS, token.IsCompound(p.tok):
		expression = p.parseAssign(location)

		// TODO: case for token.INSERTION
	}

	if p.tok != token.SEMICOLON {
		fmt.Println(p.tok, p.lit)
		p.error("Expected SEMICOLON (;) token")
	}

	p.next()
	return
}

// location = [clone, '.'], (identifier | call), {'.', (identifier | call)};
// clone = '|', location, '|';
func (p *parser) parseLocation() (location *ast.Location) {
	location = new(ast.Location)

	// If first token is a pipe, the location starts with a clone
	if p.tok == token.PIPE {
		p.next()

		location.AddSegment(&ast.Clone{p.parseLocation()})

		if p.tok != token.PIPE {
			p.error("Expected PIPE (|) token")
		}
		p.next()
	}

	for p.tok == token.IDENTIFIER {
		location.AddSegment(&ast.Identity{p.lit})

		p.next()

		// TODO: Handle calls

		// TODO: Handle (lack of) token.PERIOD
	}

	return
}

// parseCall

func (p *parser) parseAssign(location *ast.Location) object.Expression {
	if token.IsCompound(p.tok) {
		// TODO: get the operation for later use (gen the struct now?)
	} else if p.tok != token.EQUALS {
		p.error("Expected EQUALS (=) or compound assignment token")
	}

	// Eat assignment token
	p.next()

	formula := p.parseFormula()

	// TODO: Wrap formula in operation if compound

	return &ast.Assign{location, formula}
}

// parseInsert

//formula = value, {operation, value};
func (p *parser) parseFormula() ast.Evaluable {
	return p.parseFormulaPrecedence(p.parseUnary(), 0)
}

func (p *parser) parseFormulaPrecedence(left ast.Evaluable, lastPrec int) ast.Evaluable {
	// Precedence-based parsing
	for {
		operator := p.tok

		prec := token.GetPrecedence(operator)
		if prec < lastPrec {
			return left
		}

		p.next()

		right := p.parseUnary()

		if prec < token.GetPrecedence(p.tok) {
			right = p.parseFormulaPrecedence(right, prec+1)
		}

		left = &ast.Operation{operator, left, right}
	}

	return left
}

// unary_operation = {unary_operator}, value;
// unary_operator = '!' | '-';
func (p *parser) parseUnary() ast.Evaluable {
	if !token.IsUnary(p.tok) {
		return p.parseValue()
	}

	operator := p.tok
	p.next()
	return &ast.Unary{operator, p.parseUnary()}
}

// value = number
//       | string
//       | boolean
//       | null
//       | group
//       | location
//       | call
//       | definition;
func (p *parser) parseValue() (value ast.Evaluable) {
	// TODO: the obvious
	switch p.tok {
	case token.NUMBER:
		f, _ := strconv.ParseFloat(p.lit, 64)
		value = &ast.LiteralNumber{f}
		p.next()

	case token.STRING:
	case token.TRUE:
	case token.FALSE:
	case token.NULL:

	// Grouping: Delegate due to amiguous syntax
	case token.PAREN_LEFT:
		value = p.parseParen()

	case token.BRACE_LEFT:
	case token.IDENTIFIER, token.PIPE:
	default:
		p.error("TODO: Think up an appropriate error message")
	}

	return
}

func (p *parser) parseParen() ast.Evaluable {
	pos := p.pos
	p.next()

	// Find the first token after closing paren
	nested := 1
	for nested > 0 {
		if p.tok == token.PAREN_LEFT {
			nested += 1
		} else if p.tok == token.PAREN_RIGHT {
			nested -= 1
		}
		p.next()
	}

	// Get the token, then jump back to the beginning
	tok := p.tok
	p.lexer.Jump(pos)
	p.next()

	// If it was a left brace, it's a function.
	if tok == token.BRACE_LEFT {
		return p.parseDefinition()
	}

	p.next()
	formula := p.parseFormula()
	p.next()
	return formula
}

// definition = [parameters], '{', body, '}';
func (p *parser) parseDefinition() ast.Evaluable {
	params := make([]string, 0)

	// starts on a paren, parse params
	if p.tok == token.PAREN_LEFT {
		params = p.parseParameters()
	}

	if p.tok != token.BRACE_LEFT {
		p.error("Expected BRACE_LEFT ({) token")
	}
	p.next()

	body := p.parseBody(token.BRACE_RIGHT)
	return &ast.Definition{params, body}
}

// parameters = '(', identifier, {',', identifier}, '}';
func (p *parser) parseParameters() []string {
	p.next()

	params := make([]string, 0)
	for p.tok == token.IDENTIFIER {
		params = append(params, p.lit)

		p.next()
		if p.tok != token.COMMA {
			break
		}
		p.next()
	}
	if p.tok != token.PAREN_RIGHT {
		p.error("Expected PAREN_RIGHT ()) token")
	}
	p.next()

	return params
}

func (p *parser) next() {
	p.pos, p.tok, p.lit = p.lexer.Next()
}

func (p *parser) error(message string) {
	panic(message)
}
