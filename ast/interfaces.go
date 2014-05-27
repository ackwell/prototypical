package ast

type Expression interface {
	execute()
}

type Evaluable interface {
	evaluate()
}

type Assignable interface {
	assign()
}


type LocationSegment interface {

}
