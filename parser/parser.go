package parser

import (
	"github.com/ackwell/prototypical/lexer"
	"github.com/ackwell/prototypical/token"
	"github.com/ackwell/prototypical/ast"
	"strconv"
	"fmt"
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
func (p *parser) parseBody(end token.Token) (body []ast.Expression) {
	// Capture expressions until reach end token
	for p.tok != end {
		body = append(body, p.parseExpression())
	}

	// Eat the end token
	p.next()

	return body
}

// expression = location, [assign | insert];
func (p *parser) parseExpression() (expression ast.Expression) {
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

func (p *parser) parseAssign(location *ast.Location) ast.Expression {
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
			right = p.parseFormulaPrecedence(right, prec + 1)
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
	case token.PAREN_LEFT:
	case token.BRACE_LEFT:
	case token.IDENTIFIER, token.PIPE:
	default:
		p.error("TODO: Think up an appropriate error message")
	}

	return
}

// parseParen

// parseDefinition

// parseParameters

func (p *parser) next() {
	p.pos, p.tok, p.lit = p.lexer.Next()
	fmt.Println(p.pos, p.tok, p.lit)
}

func (p *parser) error(message string) {
	panic(message)
}
